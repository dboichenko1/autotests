result = [{'basicstudies': {'GNuvT7h0': True, 'zJlhAtff': True, 'lPS6jvVP': True, 'NzOOaaky_nonseries/st1': True, 'NzOOaaky_nonseries/st2': True, 'NzOOaaky_nonseries/st3': True, 'NzOOaaky_nonseries/st4': True, 'NzOOaaky_nonseries/st5': True, 'NzOOaaky_nonseries/st6': True, 'NzOOaaky_nonseries/st7': True, 'NzOOaaky_nonseries/st8': True, 'NzOOaaky_nonseries/st9': True, 'NzOOaaky_nonseries/st10': True, 'NzOOaaky_nonseries/st11': True, 'NzOOaaky_nonseries/st12': True, 'NzOOaaky_nonseries/st13': True, 'NzOOaaky_nonseries/st14': True, 'NzOOaaky_nonseries/st15': True, 'NzOOaaky_nonseries/st16': True, 'NzOOaaky': True}}]
for i in result:
    for key,value in i.items():
        print(f'\n{key.upper()}')
        for k,v in value.items():
            print(f'{k} : {v}')