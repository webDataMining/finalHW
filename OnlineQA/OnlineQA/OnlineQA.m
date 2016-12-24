//
//  OnlineQA.m
//  OnlineQA
//
//  Created by 范志康 on 2016/12/22.
//  Copyright © 2016年 范志康. All rights reserved.
//

#import "OnlineQA.h"

#define FAIL_COUNT_MAX 5

@implementation OnlineQA {
    NSUInteger failCount;
    BOOL shouldSleep;
    NSUInteger timeInterval;
    NSUInteger urlIndex;
    NSArray *URLs;
}

- (void)start {
    failCount = 0;
    shouldSleep = NO;
    timeInterval = 0;
    urlIndex = 0;
    URLs = @[@"http://localhost/~Frank/search/api/",
             @"http://search.fanzhikang.cn/api/"];
    
    NSString *questionsString = [self _readFileAtPath:@"answers-final.txt"];
    assert(questionsString);
    NSArray<NSString *> *questionsArray = [questionsString componentsSeparatedByString:@"\r\n"];
    NSMutableDictionary *answersCache = [NSMutableDictionary dictionary];
    NSMutableString *outputString = [NSMutableString string];
    NSMutableString *outputHTML = [NSMutableString stringWithString:@"<!DOCTYPE html>\n<html lang='en'>\n<head>\n\t<meta charset='UTF-8'>\n\t<style>\n\t\ttable{width:100%;table-layout:fixed}\n\t\ttd{white-space:nowrap;overflow:hidden;word-break:keep-all;text-overflow:ellipsis}\n\t</style>\n</head>\n<body>\n<table>\n"];
    
    __block NSUInteger recommendNum = 0, YZDDMatchNum = 0, YZDDMismatchNum = 0;
    [questionsArray enumerateObjectsUsingBlock:^(NSString * _Nonnull obj, NSUInteger idx, BOOL * _Nonnull stop) {
        NSArray *questionLine = [obj componentsSeparatedByString:@"\t"];
        if (questionLine.count < 2) {
            return;
        }
        NSInteger number = [questionLine[0] integerValue];
        NSString *question = questionLine[1];
        NSString *answer = questionLine.count > 2 ? questionLine[2] : @"";
        if (answersCache[question]) {
//            NSLog(@"Cache hit %ld: '%@'", number, question);
            answer = answersCache[question];
        } else if (![self _needProcessAgain:answer]) {
//            NSLog(@"Skipping %ld: %@", number, question);
            answersCache[question] = answer;
        } else {
            if (failCount >= FAIL_COUNT_MAX) {
                for (int i = 0; i < 60 && shouldSleep; i++) {
                    NSLog(@"Program sleeping...");
                    [NSThread sleepForTimeInterval:60];
                }
                if (shouldSleep) {
                    failCount = 0;
                    urlIndex ++;
                    if (urlIndex >= URLs.count) {
                        urlIndex = 0;
                    }
                }
            }
            NSLog(@"Processing %ld: %@", number, question);
            if (failCount < FAIL_COUNT_MAX) {
                answer = [self _processQuestion:question onlyShowRecommend:NO];
                answer = [answer stringByReplacingOccurrencesOfString:@"(\n|\r|\t)" withString:@"" options:NSRegularExpressionSearch range:NSMakeRange(0, answer.length)];
//                if ([answer rangeOfString:@"一站到底"].location != NSNotFound) {
//                    NSString *YZDDAnswer = [self _findYZDDWithQuestion:question andAnswer:answer];
//                    if (YZDDAnswer.length > 0) {
////                        NSLog(@"%@", YZDDAnswer);
//                        answer = YZDDAnswer;
//                        YZDDMatchNum++;
//                    } else {
////                        NSLog(@"%@\n%@", question, answer);
//                        YZDDMismatchNum++;
//                    }
//                } else if ([self _isRecommend:answer]) {
//                    recommendNum++;
//                }
                // 随机间隔一段时间，防止爬虫IP被封
                if (timeInterval > 0) {
                    [NSThread sleepForTimeInterval:1 + arc4random() % timeInterval];
                }
            } else {
                answer = @"";
            }
            answersCache[question] = answer;
        }
        if ([self _needProcessAgain:answer]) {
            failCount ++;
        } else {
            if (failCount > 0) {
                failCount --;
            }
        }
        [outputString appendString:[NSString stringWithFormat:@"%ld\t%@\t%@\r\n", number, question, answer]];
        [outputHTML appendString:[NSString stringWithFormat:@"\t<tr>\n\t\t<td style='width:5%%'>%ld</td>\n\t\t<td style='width:50%%'>%@</td>\n\t\t<td style='width:45%%%@'>%@</td>\n\t</tr>\n", number, question, [self _isRecommend:answer] ? @";color:green" : @"",answer]];
    }];
    [outputHTML appendString:@"</table>\n</body>\n</html>"];
    [self _writeFile:outputString toPath:@"answers-final.txt"];
    [self _writeFile:outputHTML toPath:@"answers-final.html"];
    NSLog(@"Recommend: %ld, YZDD Match: %ld, YZDD Mismatch: %ld", recommendNum, YZDDMatchNum, YZDDMismatchNum);
}

- (NSString *)_processQuestion:(NSString *)question onlyShowRecommend:(BOOL)onlyShowRecommend {
    NSDictionary *rawAnswer = [self _queryAPIWith:question];
    if (!rawAnswer) {
        return @"";
    }
    if ([rawAnswer[@"recommends"] count] > 0) {
        return [self _formBestRecommend:rawAnswer[@"recommends"]];
    } else {
        NSString *searchResult;
        NSArray<NSString *> *warnings = rawAnswer[@"warnings"];
        NSString *rawResult = [self _formAnswerFromResults:rawAnswer[@"results"]];
        if (warnings.count > 0) {
            [warnings enumerateObjectsUsingBlock:^(NSString * _Nonnull obj, NSUInteger idx, BOOL * _Nonnull stop) {
                NSLog(@"Warning: %@", obj);
            }];
            searchResult = [NSString stringWithFormat:@"{{%@}}", rawResult];
        } else {
            searchResult = [NSString stringWithFormat:@"[[%@]]", rawResult];
        }
        
        NSDictionary<NSString *, NSString *> *regExps;
        regExps = @{@".*?“(.*?)”.*?((下|上|前|后)(一|两|半)?句)": @"$1 的$2",
                    @".*?《(.|[^《]*?)》(是|出自).*?的.*?(歌|曲).*": @"“$1” 是谁唱的",
                    @".*?《(.|[^《]*?)》(是|出自).*?的.*?(诗|作|书|文).*": @"“$1” 的作者是谁"
                    };

        __block NSString *newQuestion = question;
        [regExps enumerateKeysAndObjectsUsingBlock:^(NSString * _Nonnull key, NSString * _Nonnull obj, BOOL * _Nonnull stop) {
            newQuestion = [newQuestion stringByReplacingOccurrencesOfString:key withString:obj options:NSRegularExpressionSearch range:NSMakeRange(0, newQuestion.length)];
        }];
        
        if ([newQuestion isEqualToString:question]) { // 没有找到可重定向的问题
            if (onlyShowRecommend) {
                return @"";
            } else {
                return searchResult;
            }
        } else {
            NSLog(@"Redirecting to: %@", newQuestion);
            NSString *recommend = [self _processQuestion:newQuestion onlyShowRecommend:YES];
            // 如果没有找到推荐，返回原始查询结果
            return recommend.length > 0 ? recommend : onlyShowRecommend ? @"" : searchResult;
        }
    }
}

- (NSString *)_findYZDDWithQuestion:(NSString *)question andAnswer:(NSString *)answer {
    NSMutableDictionary<NSString *, NSNumber *> *answersCount = [NSMutableDictionary dictionary];
    void(^addAnswer)(NSString *) = ^(NSString *recommend) {
        recommend = [self _cleanYZDDAnswer:recommend];
        if (recommend.length == 0) {
            return;
        }
        NSNumber *count = answersCount[recommend];
        if (count) {
            count = @([count integerValue] + 1);
        } else {
            count = @(1);
        }
        answersCount[recommend] = count;
    };
    
    NSDictionary<NSString *, NSString *> *characterReplacements;
    characterReplacements = @{@"，": @",",
                              @"。": @".",
                              @"？": @"?",
                              @"：": @":",
                              @"＊": @"*",
                              @"“": @"\"",
                              @"”": @"\"",
                              @"‘": @"'",
                              @"’": @"'",
                              @"（": @"(",
                              @"）": @")",
                              @" ": @"",
                              @"哪一": @"哪",
                              @"那": @"哪", // 原文偶尔有错误
                              @"着有": @"著有" // 问题偶尔有错
                              };
    for (NSString *text in @[question, answer]) {
        __block NSString *newText = text;
        [characterReplacements enumerateKeysAndObjectsUsingBlock:^(NSString * _Nonnull key, NSString * _Nonnull obj, BOOL * _Nonnull stop) {
            newText = [newText stringByReplacingOccurrencesOfString:key withString:obj];
        }];
        if ([text isEqualToString:question]) {
            question = newText;
        } else {
            answer = newText;
        }
    }
    
    NSRegularExpression *regex = [NSRegularExpression regularExpressionWithPattern:[NSString stringWithFormat:@"([0-9]{1,3})[.|:|：|、] ?%@(.*?)([0-9]{1,3})", question] options:NSRegularExpressionCaseInsensitive error:nil];
    NSArray<NSTextCheckingResult *> *matches = [regex matchesInString:answer options:NSMatchingReportCompletion range:NSMakeRange(0, answer.length)];
    if (matches.count > 0) {
        [matches enumerateObjectsUsingBlock:^(NSTextCheckingResult * _Nonnull obj, NSUInteger idx, BOOL * _Nonnull stop) {
            NSInteger currentNum = [[answer substringWithRange:[obj rangeAtIndex:1]] integerValue];
            NSInteger nextNum = [[answer substringWithRange:[obj rangeAtIndex:3]] integerValue];
            if (nextNum == currentNum + 1) {
                NSString *recommend = [answer substringWithRange:[obj rangeAtIndex:2]];
                addAnswer(recommend);
            }
        }];
    }
    
    if (answersCount.count > 0) {
        NSArray<NSString *> *sortedAnswer = [answersCount keysSortedByValueUsingComparator:^NSComparisonResult(id  _Nonnull obj1, id  _Nonnull obj2) {
            return [obj2 compare:obj1];
        }];
        __block NSString *bestAnswer;
        [sortedAnswer enumerateObjectsUsingBlock:^(NSString * _Nonnull obj, NSUInteger idx, BOOL * _Nonnull stop) {
            if (![obj containsString:@"一站到底"] && obj.length < 10) {
                bestAnswer = obj;
                *stop = YES;
            }
        }];
        return bestAnswer;
    } else {
        return nil;
    }
}

- (NSString *)_cleanYZDDAnswer:(NSString *)answer {
    NSString *originalAnswer;
    while (true) {
        originalAnswer = answer;
        answer = [answer stringByReplacingOccurrencesOfString:@"^[\\?|:|;|；|答案?]" withString:@"" options:NSRegularExpressionSearch range:NSMakeRange(0, answer.length)];
        answer = [answer stringByReplacingOccurrencesOfString:@"^[•|\\-|_]*|[•|\\-|_]*$" withString:@"" options:NSRegularExpressionSearch range:NSMakeRange(0, answer.length)];
        answer = [answer stringByReplacingOccurrencesOfString:@"^[\\(|【|\\[](.*?)[\\)|】|\\]]$" withString:@"$1" options:NSRegularExpressionSearch range:NSMakeRange(0, answer.length)];
        if ([answer isEqualToString:originalAnswer]) {
            break;
        }
    }
    return answer;
}

- (NSDictionary *)_queryAPIWith:(NSString *)question {
    NSString *queryURL = [NSString stringWithFormat:@"%@?range=online&text=%@", URLs[urlIndex], [question stringByAddingPercentEncodingWithAllowedCharacters:[NSCharacterSet URLQueryAllowedCharacterSet]]];
    NSData *rawData = [NSData dataWithContentsOfURL:[NSURL URLWithString:queryURL]];
    if (!rawData) {
        return nil;
    }
    NSError *error;
    NSDictionary *rawDict = [NSJSONSerialization JSONObjectWithData:rawData options:kNilOptions error:&error];
    if (error) {
        NSLog(@"Query %@ with error: %@", question, error.localizedDescription);
        return nil;
    }
    NSInteger code = [rawDict[@"code"] integerValue];
    if (code != 0) {
        NSLog(@"Query %@ with error %ld: %@", question, code, rawDict[@"message"]);
        return nil;
    } else {
        return rawDict[@"data"];
    }
}

- (NSString *)_formBestRecommend:(NSArray<NSDictionary *> *)recommends {
    __block NSString *bestAnswer;
    [recommends enumerateObjectsUsingBlock:^(NSDictionary * _Nonnull obj, NSUInteger idx, BOOL * _Nonnull stop) {
        NSString *answer = obj[@"answer"];
        if (!bestAnswer || answer.length < bestAnswer.length) {
            bestAnswer = answer;
        }
    }];
    
    NSLog(@"Find recommend: %@", bestAnswer);
    return bestAnswer;
}

- (NSString *)_formAnswerFromResults:(NSArray<NSDictionary *> *)results {
    NSMutableArray *answer = [NSMutableArray array];
    [results enumerateObjectsUsingBlock:^(NSDictionary * _Nonnull obj, NSUInteger idx, BOOL * _Nonnull stop) {
        [answer addObject:[NSString stringWithFormat:@"%@: %@", obj[@"title"], obj[@"text"]]];
    }];
    return [answer componentsJoinedByString:@";"];
}

- (BOOL)_needProcessAgain:(NSString *)answer {
    return answer.length == 0 || ([answer hasPrefix:@"{{"] && [answer hasSuffix:@"}}"]);
}

- (BOOL)_isRecommend:(NSString *)answer {
    return ![self _needProcessAgain:answer] && !([answer hasPrefix:@"[["] && [answer hasSuffix:@"]]"]);
}

/**
 读取指定位置的文件
 
 @param fileName 文件名
 
 @return 读取的字符串
 */
- (NSString *)_readFileAtPath:(NSString *)fileName {
    NSError *readError;
    NSString *content = [NSString stringWithContentsOfFile:[RESOURCE_FOLDER stringByAppendingString:fileName] encoding:NSUTF8StringEncoding error:&readError];
    if (readError) {
        NSLog(@"Read file error: %@", readError.localizedDescription);
        return nil;
    }
    return content;
}

/**
 写入结果到指定位置
 
 @param data     要写入的字符串
 @param fileName 文件名
 */
- (void)_writeFile:(NSString *)data toPath:(NSString *)fileName {
    NSError *writeError;
    [data writeToFile:[RESULT_FOLDER stringByAppendingString:fileName] atomically:YES encoding:NSUTF8StringEncoding error:&writeError];
    if (writeError) {
        NSLog(@"Write file error: %@", writeError.localizedDescription);
    }
}

@end
