
import sympy
import json
import math
from sympy import *

factsName = ['a', 'b', 'c', 'gocA', 'gocB', 'gocC', 'ha', 'hb', 'hc', 'Area', 'p', 'R', 'r', 'sinA', 'sinB', 'sinC',
             'cosA', 'cosB', 'cosC']
facts = [None] * 19
baseKnown = []
rules = []
targets1 = []
answer = {}

def reset():
    global factsName
    global facts
    global baseKnown
    global rules
    global targets1
    global answer

    factsName = ['a', 'b', 'c', 'gocA', 'gocB', 'gocC', 'ha', 'hb', 'hc', 'Area', 'p', 'R', 'r', 'sinA', 'sinB', 'sinC',
             'cosA', 'cosB', 'cosC']
    facts = [None] * 19
    baseKnown = []
    rules = []
    targets1 = []
    answer = {}
    print('reset success!')

def run(inputdata):
    print('start')
    # doc file rules
    with open(r'rules.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for p in data['rules']:
            r = RuleClass(p['idx'], p['name'], p['concepts'], p['expression'])
            rules.append(r)

    count = 0
    # doc gia thiet
    for p in inputdata['facts']:
        facts[count] = p
        if p is not None:
            baseKnown.append(factsName[count])
        count = count +1
        #gia thiet duoi dang cac bien phu thuoc coi nhu 1 rule
    for p in inputdata['rules']:
        r = RuleClass(p['idx'], p['name'], p['concepts'], p['expression'])
        rules.append(r)
    # doc casc bien can tim
    targets1 = inputdata['targets']

    answer['answers'] = []
    # bat dau giai
    while not check_muc_tieu(targets1):
        found1 = false
        tinh_luong_giac()
        for r in rules:
            is_ready, concept_to_solve = is_ready_for_solve(r)
            if is_ready:
                found1 = true
                val = solveWithRule(r)
                tl = r.concept_list.copy()
                tl.remove(concept_to_solve)
                answer['answers'].append({
                    'idx': r.idx,
                    'name': r.name,
                    'base': tl,
                    'concept': concept_to_solve,
                    'value': val
                })
                facts[factsName.index(concept_to_solve)] = val
                tinh_luong_giac()
                if check_muc_tieu(targets1):
                    break
        if not found1:
            break

    if len(answer['answers']) < 1:
        return "no answer"
    # loai bo cac luat thua
    idxList = removeUnusedRules(answer['answers'], targets1)
    finalAns = []
    currentIdx = 0
    for ans in answer['answers']:
        if currentIdx in idxList:
            finalAns.append(ans)
        currentIdx = currentIdx + 1
    answer['answers'] = finalAns.copy()
    #loai bo 6 gia tri luong giac o cuoi cung
    #answer['facts'] = facts[:-6]
    # output answer, facts
    with open(r'answer.json', 'w') as outfile:
        json.dump(answer, outfile)
    print('end')
    return answer

# check xem muc tieu da thoa man hay chua
def check_muc_tieu(targets):
    for t in targets:
        if getConceptValue(t) is None:
            return false
    return true

# check xem rule nay co the sinh ra su kien moi hay khong
# neu bieu thuc chi con 1 bien chua biet -> true
def is_ready_for_solve(rule):
    if rule.used == true:
        return false, ''
    count = 0
    concept_can_be_solve = ''
    for c in rule.concept_list:
        if getConceptValue(c) is not None:
            count += 1
        else:
            concept_can_be_solve = c
    return rule.concept_count == count + 1, concept_can_be_solve

# tinh gia tri con thieu trong rule
def solveWithRule(rule):
    expr = simplify(rule.expression)
    for c in rule.concept_list:
        expr = expr.subs(c, getConceptValue(c))
    val = sympy.solve(expr)
    rule.used = true
    if len(val) == 1:
        return convert(val[0])
    if len(val) > 1:
        for v in val:
            if v > 0:
                return convert(v)
    return val

# ham tinh gia tri luong giac tu so do goc va nguoc lai
def tinh_luong_giac():
    gocA = getConceptValue('gocA')
    gocB = getConceptValue('gocB')
    gocC = getConceptValue('gocC')
    sinA = getConceptValue('sinA')
    sinB = getConceptValue('sinB')
    sinC = getConceptValue('sinC')
    cosA = getConceptValue('cosA')
    cosB = getConceptValue('cosB')
    cosC = getConceptValue('cosC')

    if sinA is not None and gocA is None:
        gocA = convert(math.degrees(math.asin(sinA)))
        answer['answers'].append({
            'idx': 0,
            'base': ['sinA'],
            'concept': 'gocA',
            'value': gocA
        })
    elif cosA is not None and gocA is None:
        gocA = convert(math.degrees(math.acos(cosA)))
        answer['answers'].append({
            'idx': 0,
            'base': ['cosA'],
            'concept': 'gocA',
            'value': gocA
        })

    if sinB is not None and gocB is None:
        gocB = convert(math.degrees(math.asin(sinB)))
        answer['answers'].append({
            'idx': 0,
            'base': ['sinB'],
            'concept': 'gocB',
            'value': gocB
        })
    elif cosB is not None and gocB is None:
        gocB = convert(math.degrees(math.acos(cosB)))
        answer['answers'].append({
            'idx': 0,
            'base': ['cosB'],
            'concept': 'gocB',
            'value': gocB
        })

    if sinC is not None and gocC is None:
        gocC = convert(math.degrees(math.asin(sinC)))
        answer['answers'].append({
            'idx': 0,
            'base': ['sinC'],
            'concept': 'gocC',
            'value': gocC
        })
    elif cosC is not None and gocC is None:
        gocC = convert(math.degrees(math.acos(cosC)))
        answer['answers'].append({
            'idx': 0,
            'base': ['cosC'],
            'concept': 'gocC',
            'value': gocC
        })

    if gocA is not None:
        if sinA is None:
            sinA = convert(math.sin(math.radians(gocA)))
            answer['answers'].append({
                'idx': 0,
                'base': ['gocA'],
                'concept': 'sinA',
                'value': sinA
            })
        if cosA is None:
            cosA = convert(math.cos(math.radians(gocA)))
            answer['answers'].append({
                'idx': 0,
                'base': ['gocA'],
                'concept': 'cosA',
                'value': cosA
            })

    if gocB is not None:
        if sinB is None:
            sinB = convert(math.sin(math.radians(gocB)))
            answer['answers'].append({
                'idx': 0,
                'base': ['gocB'],
                'concept': 'sinB',
                'value': sinB
            })
        if cosB is None:
            cosB = convert(math.cos(math.radians(gocB)))
            answer['answers'].append({
                'idx': 0,
                'base': ['gocB'],
                'concept': 'cosB',
                'value': cosB
            })

    if gocC is not None:
        if sinC is None:
            sinC = convert(math.sin(math.radians(gocC)))
            answer['answers'].append({
                'idx': 0,
                'base': ['gocC'],
                'concept': 'sinC',
                'value': sinC
            })
        if cosC is None:
            cosC = convert(math.cos(math.radians(gocC)))
            answer['answers'].append({
                'idx': 0,
                'base': ['gocC'],
                'concept': 'cosC',
                'value': cosC
            })

    facts[factsName.index('gocA')] = gocA
    facts[factsName.index('gocB')] = gocB
    facts[factsName.index('gocC')] = gocC
    facts[factsName.index('sinA')] = sinA
    facts[factsName.index('sinB')] = sinB
    facts[factsName.index('sinC')] = sinC
    facts[factsName.index('cosA')] = cosA
    facts[factsName.index('cosB')] = cosB
    facts[factsName.index('cosC')] = cosC

#lay gia tri concept dua vao ten concept
def getConceptValue(fname):
    return facts[factsName.index(fname)]

#ham lam tron so va convert phan so thanh so thap phan
def convert(s):
    val = 0.000
    if s is None:
        return s
    try:
        val = float(s)
    except ValueError:
        num, denom = s.split('/')
        val = float(num) / float(denom)
    val = round(val, 4)
    return val

# xoa bo cac luat thua
def removeUnusedRules(tempAns, targets1):
    resultAns = []
    tempTarget = targets1.copy()
    while len(tempTarget) > 0:
        currentIdx = 0
        for ans in tempAns:
            if ans['concept'] in tempTarget:
                #r = getRule(ans['idx'])
                #for c in r['concepts']:
                #    if c not in tempTarget and c not in baseKnown:
                #        tempTarget.append(c)
                for c in ans['base']:
                    if c not in tempTarget and c not in baseKnown:
                        tempTarget.append(c)
                tempTarget.remove(ans['concept'])
                resultAns.append(currentIdx)
            currentIdx = currentIdx + 1

    return resultAns

def getRule(idx):
    for r in rules:
        if r.idx == idx:
            return r

def isListContaintConcept(list, c):
    for item in list:
        t1 = item.replace('sinA','gocA').replace('sinB','gocB').replace('sinC','gocC').replace('cosA','gocA').replace('cosB','gocB').replace('cosC','gocC')
        c1 = c.replace('sinA','gocA').replace('sinB','gocB').replace('sinC','gocC').replace('cosA','gocA').replace('cosB','gocB').replace('cosC','gocC')
        if c1 == t1:
            return true
    return false

#cau truc cac rule, bao gom
#               idx: index cua rule trong file rules.json
#      concept_list: cac concept xuat hien trong rule nay
#        expression: bieu thuc tinh, gia tri bieu thuc luon =0
#     concept_count: so luong concept trong bieu thuc
class RuleClass(object):
    def __init__(self, idx, name, concept_list, expression):
        self.idx = idx
        self.name = name
        self.concept_list = concept_list
        self.expression = expression
        self.concept_count = len(concept_list)
        self.used = false
