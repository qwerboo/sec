from entity import *

def obj_to_dict(obj):
    ''' 对象转字典 '''
    dic = dict()
    for k,v in obj.__dict__.items():
        if not isinstance(v, list):
            dic[k[:-1]] = v
    return dic

if __name__ == '__main__':
    p = Person()
    p.name = 'hello'
    person = obj_to_dict(p)
    print(person)
