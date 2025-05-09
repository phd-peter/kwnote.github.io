from pyparsing import nestedExpr, Word, alphanums, Literal, ParserElement

ParserElement.enablePackrat()

def parse_over_expression(text):
    # 중첩된 {}를 파싱하는 parser 정의
    brace_expr = nestedExpr('{', '}')

    # 전체 수식을 {} 단위로 파싱
    parsed = brace_expr.parseString('{' + text + '}').asList()[0]

    def process(parsed_list):
        result = ''
        i = 0
        while i < len(parsed_list):
            item = parsed_list[i]
            if isinstance(item, list) and i + 1 < len(parsed_list) and parsed_list[i + 1] == 'over' and i + 2 < len(parsed_list):
                # \frac 변환 처리
                left = process(item)
                right = process(parsed_list[i + 2])
                result += f"\\frac{{{left}}}{{{right}}}"
                i += 3  # skip over + right
            else:
                if isinstance(item, list):
                    result += '{' + process(item) + '}'
                else:
                    result += item
                i += 1
        return result

    return process(parsed)

# 테스트
example = "{ { a } } over { b } + { x } over { { y } + { z } }"
converted = parse_over_expression(example)
print(converted)
