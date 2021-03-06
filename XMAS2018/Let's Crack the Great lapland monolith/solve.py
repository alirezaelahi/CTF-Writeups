
import requests
from fractions import *
import re

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist for %d %d' % (a, m))
    else:
        return x % m

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment

def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * modinv(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)

def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return crack_unknown_multiplier(states, modulus)


#modulus
#multiplier
#increment


#s1 = (s0*m + c) % n



def get_cookie():   
    r = requests.get("http://45.76.90.207:12000")
    return requests.utils.dict_from_cookiejar(r.cookies)


cookies = get_cookie()
def guess(number, debug=False):
    r = requests.get("http://45.76.90.207:12000/?guess=" + str(number), cookies=cookies)
    answer = re.search(r':<br>(.*?)<',r.text).group(1)
    if debug:
        print r.text
        if "Wrong guess" in r.text:
            raise Exception("Try again")
    return answer


numbers = []

for i in range(8):
	numbers.append(int(guess(i)))

print "Cracking these numbers: "
print numbers


(n,m,c) = crack_unknown_modulus(numbers)

print "N=%d" % n
print "m=%d" % m
print "c=%d" % c



start = int(guess(1,False))
print start


for i in range(20):
	sn = (start*m + c) % n
	print "Predicting next number is %d" % sn
	start = int(guess(sn,True))