# Automatic Zacate game player
# B551 Fall 2015
# PUT YOUR NAME AND USER ID HERE!
#
# Based on skeleton code by D. Crandall
#
# PUT YOUR REPORT HERE!
#
#
# This is the file you should modify to create your new smart Zacate player.
# The main program calls this program three times for each turn. 
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list 
#      of dice indices that should be re-rolled.
#   
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that 
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#

"""
Report:
This program greedily chooses categories. It chooses the unused category that gives the highest score for the round.
In a way this code is myopic but it still gives good experimental results. Moreover, looking beyond one round takes too much time due to the high branching factor.
Aso, the high branching factor increase the space complexity of expectiminmax tree.

Hence, for reduce time and space complexity, only the current roll is considered.

In this program we try to select dice to be rerolled based on expected scores. We select the combination of dices that has highest expected score.
Following is list of combinations of dice to reroll:
[[], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4], [0, 1, 2, 4], [0, 1, 3], [0, 1, 3, 4], [0, 1, 4], [0, 2], [0, 2, 3], [0, 2, 3, 4], [0, 2, 4], [0, 3], [0, 3, 4], [0, 4], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 4], [1, 3], [1, 3, 4], [1, 4], [2], [2, 3], [2, 3, 4], [2, 4], [3], [3, 4], [4]];

Expected score = (Sum of all scores possible)*((1/6)^no. of dice rerolled)

While checking all possible dice rerolls will give us the best answer, its very slow due to high computation required.

Intuitively, we know that the point of the rerolls is to improve the score from original roll. Hence, we never reroll all dice.

I had originally written code that checked all possible combinations (upto 4 dice rerolled at a time). But complexity of that program was O(n^4).

Also, i noticed the higher number of dice to be rerolled are rarely choosen.
This is because their probabilty is much lower and hence the chances of reaching a possible more favourable state is much lower.

Moreover, just rerolling two dice in two rerolls gives us all possible combinations of upto rerolling 4 dice.

Hence, to reduce computation time we reroll maximum only 2 dice at a time.

Then we pick the combination that gives us the best expected score from rerolling no dice, rerolling one die and rerolling 2 dice.

Method expvalue accepts a reroll choice of dice and returns expected score.

This program took about 4 mins to produce output for a 100 iterations.

P.S. Just for reference when upto 3 rerolls were done, a much slower program gave this output:
Min/max/mean scores: 137 318 211.23

"""
import copy
import math

from ZacateState import Dice
from ZacateState import Scorecard
import random

class Node:#creates node for each dice n scorecard instance.
      def __init__(self,d,scorecard,dice):
            self.depth=d;
            self.scoretillnow=scorecard;
            self.dicenow=dice;
            if(self.depth!=3):
                  self.childnodes=[[], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4], [0, 1, 2, 4], [0, 1, 3], [0, 1, 3, 4], [0, 1, 4], [0, 2], [0, 2, 3], [0, 2, 3, 4], [0, 2, 4], [0, 3], [0, 3, 4], [0, 4], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 4], [1, 3], [1, 3, 4], [1, 4], [2], [2, 3], [2, 3, 4], [2, 4], [3], [3, 4], [4]];
                  #childnodes contains all possible choices of ways in which dice can be selected
                  self.childexpvalue=self.expvalues();
                  #this contains expected scores from rolling dices corresponding to childnodes.
      def expvalues(self):
            evs=[];
            for i in self.childnodes:
                  evs.append(self.expvalue(i));
            return evs

      def expvalue(self,i):

            l=len(i);
            p=math.pow((1.0/6),l)
            sumcat=0;

            if len(i)==0:
                  dicenext=copy.deepcopy(self.dicenow);
                  maxicat="";
                  maxi=0;
                  for k in list(set(Scorecard.Categories) - set(self.scoretillnow.scorecard.keys())):
                              b=copy.deepcopy(self.scoretillnow);
                              b.record(k, dicenext);
                              if b.totalscore>=maxi:
                                          maxi=b.totalscore;
                                          maxicat=k;
                  b=copy.deepcopy(self.scoretillnow);
                  b.record(maxicat, dicenext);
                  sumcat+=b.totalscore;
            if len(i)==1:
                  for j in range(1,7):
                        dicenext=copy.deepcopy(self.dicenow);
                        dicenext.dice[i[0]]=j;
                        maxicat="";
                        maxi=0;
                        for k in list(set(Scorecard.Categories) - set(self.scoretillnow.scorecard.keys())):
                                    b=copy.deepcopy(self.scoretillnow);
                                    b.record(k, dicenext);
                                    if b.totalscore>=maxi:
                                          maxi=b.totalscore;
                                          maxicat=k;
                        b=copy.deepcopy(self.scoretillnow);
                        b.record(maxicat, dicenext);
                        sumcat+=b.totalscore;
            if len(i)==2:
                  for j in range(1,7):
                        for l in range (1,7):
                              dicenext=copy.deepcopy(self.dicenow);
                              dicenext.dice[i[0]]=j;
                              dicenext.dice[i[1]]=l;
                              maxicat="";
                              maxi=0;
                              for k in list(set(Scorecard.Categories) - set(self.scoretillnow.scorecard.keys())):
                                    b=copy.deepcopy(self.scoretillnow);
                                    b.record(k, dicenext);
                                    if b.totalscore>=maxi:
                                          maxi=b.totalscore;
                                          maxicat=k;
                              b=copy.deepcopy(self.scoretillnow);
                              b.record(maxicat, dicenext);
                              sumcat+=b.totalscore;
            '''if len(i)==3:
                  for j in range(1,7):
                        for l in range (1,7):
                              for m in range (1,7):
                                    dicenext=copy.deepcopy(self.dicenow);
                                    dicenext.dice[i[0]]=j;
                                    dicenext.dice[i[1]]=l;
                                    dicenext.dice[i[2]]=m;
                                    maxicat="";
                                    maxi=0;
                                    for k in list(set(Scorecard.Categories) - set(self.scoretillnow.scorecard.keys())):
                                          b=copy.deepcopy(self.scoretillnow);
                                          b.record(k, dicenext);
                                          if b.totalscore>=maxi:
                                                maxi=b.totalscore;
                                                maxicat=k;
                                    b=copy.deepcopy(self.scoretillnow);
                                    b.record(maxicat, dicenext);
                                    sumcat+=b.totalscore;'''
            """if len(i)==4:
                  for j in range(1,7):
                        for l in range (1,7):
                              for m in range (1,7):
                                    for n in range(1,7):
                                          dicenext=copy.deepcopy(self.dicenow);
                                          dicenext.dice[i[0]]=j;
                                          dicenext.dice[i[1]]=l;
                                          dicenext.dice[i[2]]=m;
                                          maxicat="";
                                          maxi=0;
                                          for k in list(set(Scorecard.Categories) - set(self.scoretillnow.scorecard.keys())):
                                                b=copy.deepcopy(self.scoretillnow);
                                                b.record(k, dicenext);
                                                if b.totalscore>=maxi:
                                                      maxi=b.totalscore;
                                                      maxicat=k;
                                          b=copy.deepcopy(self.scoretillnow);
                                          b.record(maxicat, dicenext);
                                          sumcat+=b.totalscore;"""

            return sumcat*p





      def children(self):
            c=[[]]
            for i in range (0,5):
                  c.append([i])
                  for j in range(i+1,5):
                        c.append([i,j])
                        for k in range(j+1,5):
                              c.append([i,j,k])
                              for l in range(k+1,5):
                                    c.append([i,j,k,l])
                                    for m in range(l+1,5):
                                          c.append([i,j,k,l,m])
            return c


      def calculatemove(self):
            if self.depth==3:
                  maxi=self.scoretillnow.totalscore;
                  maxicat="";
                  for i in list(set(Scorecard.Categories) - set(self.scoretillnow.scorecard.keys())):
                        b=copy.deepcopy(self.scoretillnow);
                        b.record(i, self.dicenow);
                        if b.totalscore>=maxi:
                              maxi=b.totalscore;
                              maxicat=i;
                  return maxicat;



      def callreroll(self):
            if self.depth<32:
                  #maxi=self.scoretillnow.totalscore;
                  #print self.dicenow.dice;
                  #print self.childnodes;
                  #print self.childexpvalue

                  maxv=max(self.childexpvalue)
                  maxindex=self.childexpvalue.index(maxv)
                  print self.childnodes[maxindex], "  len=", len(self.childnodes[maxindex])

                  return self.childnodes[maxindex]







class ZacateAutoPlayer:

      def __init__(self):
            pass  

      def first_roll(self, dice, scorecard):
            n=Node(1,scorecard,dice);
            return n.callreroll();
            # always re-roll first die (blindly)

      def second_roll(self, dice, scorecard):
            n=Node(2,scorecard,dice);
            return n.callreroll();
            #return [1, 2] # always re-roll second and third dice (blindly)


      
      def third_roll(self, dice, scorecard):
            # stupidly just randomly choose a category to put this in
            #x = random.choice( list(set(Scorecard.Categories) - set(scorecard.scorecard.keys())) );
            n=Node(3,scorecard,dice);
            x=n.calculatemove();
            print x;
            return x;

