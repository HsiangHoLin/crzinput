import sys
import math

word = sys.argv[1].lower();
length = len(word);

def getMcount(key, word):
	match = 0;
	for i in range(length):
		if key[i] == word[i]:
			match += 1;
	return match;	

def getWVec(w):
	vec = [];
	keys = {};
	f = open("../dictgen/keycord.dat", "r");
	for line in f:
		key = line.split( );
		point = [float(key[1]), float(key[2])];
		keys[key[0]] = point;
	for i in range(length - 1):
		x = keys[word[i+1]][0] - keys[word[i]][0];
		y = keys[word[i+1]][1] - keys[word[i]][1];
		vec.append(x);
		vec.append(y);
	return vec;

def getDVec(line):
	dictVec = [];
	for i in range((length - 1)*2):
		dictVec.append(float(line.split()[i + 1]));
	return dictVec;

def getDist(dictVec, wordVec):
	dist = 0;
	for i in range((length - 1)*2):
		dist += pow(dictVec[i] - wordVec[i], 2);
	dist = math.sqrt(dist);
	return dist;

def getStd(dictVec, wordVec):
	prodx = 0;
	absD = 0;
	absW = 0;
	for i in range((length - 1)*2):
		prodx += dictVec[i] * wordVec[i];
		absD += pow(dictVec[i], 2);
		absW += pow(wordVec[i], 2);
	absD = math.sqrt(absD);
	absW = math.sqrt(absW);
	std = prodx / (absD * absW); # risky
	return std, absD, absW;

try:
	f = open("../dictgen/veclen" + str(length) + ".dict", "r");

    # ver 1
	EqualThresh = 0.001;
	maxLikely = -1.0;
	lengthDiff = 100000000;
    #

    # ver 2
	dist_least = 500;
    #

	guess1 = word;
	guess2 = word;
	wordVec = getWVec(word);
	for line in f:
		dictVec = getDVec(line);

		# ver 1
		std, absD, absW = getStd(dictVec, wordVec);
		if (std - EqualThresh) > maxLikely:
			guess1 = line.split()[0];
			maxLikely = std;
			lengthDiff = abs(absD - absW);
		elif abs(std - maxLikely) < EqualThresh:
			if abs(absW - absD) < lengthDiff:
				guess1 = line.split()[0];
				maxLikely = std;
				lengthDiff = abs(absD - absW);

		# ver 2
		matchCount = getMcount(line.split()[0], word);
		dist = getDist(dictVec, wordVec) + 20 * (length - matchCount);
		if dist < dist_least:
			guess2 = line.split()[0];
			dist_least = dist;
	print guess1;
	print guess2;

except IOError:
	print "No such dictionary.";
