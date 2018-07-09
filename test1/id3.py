#!/usr/bin/python
# coding:utf-8


import operator
from math import log


def createDataSet():
    """DateSet 基础数据集
    Args:
        无需传入参数
    Returns:
        返回数据集和对应的label标签
    """
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]

    # labels  露出水面   脚蹼
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


def calcShannonEnt(dataSet):
    """calcShannonEnt(calculate Shannon entropy 计算给定数据集的香农熵)
    Args:
        dataSet 数据集
    Returns:
        返回 每一组feature下的某个分类下，香农熵的信息期望
    """

    numEntries = len(dataSet)
    # 通过一个字典变量计算分类标签label出现的次数 (在这里就是当前dataset里， yes和no各有多少个)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        # 为所有可能的分类创建字典，如果当前的键值不存在，则扩展字典并将当前键值加入字典。每个键值都记录了当前类别出现的次数。
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1

    # 对于label标签的占比，求出label标签的香农熵
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)

    return shannonEnt

def splitDataSet(dataSet, index, value):
    """splitDataSet函数的作用其实和 del(labels[bestFeat]) 这个函数，是一样的，只不过一个针对二维list，一个针对一维list
    传入：
        dataSet = [[1, 1, 'yes'],
                   [1, 1, 'yes'],
                   [1, 0, 'no'],
                   [0, 1, 'no'],
                   [0, 1, 'no']]
        0
        0
    Return:
        retDataSet =[[1, 'no'],
                     [1, 'no']]
    """
    retDataSet = []
    for featVec in dataSet:
        # index列为value的数据集【该数据集需要排除index列】
        # 判断index列的值是否为value
        if featVec[index] == value:
            # chop out index used for splitting
            # [:index]表示前index行，即若 index 为2，就是取 featVec 的前 index 行
            reducedFeatVec = featVec[:index]
            '''
            list.append(object) 向列表中添加一个对象object，添加的是整个对象
            list.extend(sequence) 把一个序列seq的内容添加到列表中，添加的是内容
            result = []
            result.extend([1,2,3])
            result.append([4,5,6])
            result.extend([7,8,9])
            结果：
            [1, 2, 3]
            [1, 2, 3, [4, 5, 6]]
            [1, 2, 3, [4, 5, 6], 7, 8, 9]
            '''
            reducedFeatVec.extend(featVec[index + 1:])
            # [index+1:]表示从跳过 index 的 index+1行，取接下来的数据
            # 收集结果值 index列为value的行【该行需要排除index列】
            retDataSet.append(reducedFeatVec)

    return retDataSet


def chooseBestFeatureToSplit(dataSet):
    """chooseBestFeatureToSplit(选择最好的特征)
    Args:
        dataSet 数据集
    Returns:
        bestFeature 最优的特征列
    """
    # 求第一行有多少列的 Feature, 最后一列是label列
    # print labels
    numFeatures = len(dataSet[0]) - 1
    # print numFeatures
    # label的信息熵#####################################当前的熵
    baseEntropy = calcShannonEnt(dataSet)
    # 最优的信息增益值, 和最优的Featurn编号
    bestInfoGain, bestFeature = 0.0, -1
    # iterate over all the features
    for i in range(numFeatures):
        # 获取  每一个实例    的第i个feature，    组成一个list
        featList = [example[i] for example in dataSet]  # 这行代码太帅了！！！
        # 使用set去重
        uniqueVals = set(featList)
        # 创建一个临时的信息熵
        newEntropy = 0.0
        # 遍历某一列的value集合，计算该列的信息熵
        # 遍历当前特征中的所有唯一属性值，对每个唯一属性值划分一次数据集，计算数据集的新熵值，并对所有唯一特征值得到的熵求和。
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value) ##################################通过splitDataSet来实验，并不是真的分割dataset!!!!!!!!
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)  #############################分组之后的熵
        # gain[信息增益]: 划分数据集前后的信息变化， 获取信息熵最大的值
        # 信息增益是熵的减少或者是数据无序度的减少。最后，比较所有特征中的信息增益，返回最好特征划分的索引值。
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
            print 'bestInfoGain=', bestInfoGain, 'bestFeature=', bestFeature
    return bestFeature


def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    # ！！！！！！！！！！！！！！！！！！！！！！！！ID3算法 递归的停止规则：增益为零. (每个叶子节点就会执行一次)！！！！！
    # 停止条件：如果数据集的最后一列的第一个值出现的次数=整个集合的数量，也就说所有的类标签完全相同
    # count() 函数是统计括号中的值在list中出现的次数
    if classList.count(classList[0]) == len(classList):
        return classList[0]

    # 选择最优的列，得到最优列对应的label含义
    bestFeat = chooseBestFeatureToSplit(dataSet)
    # 获取label的名称
    bestFeatLabel = labels[bestFeat]

    # 初始化myTree
    myTree = {bestFeatLabel: {}}

    # 根据最优列的值做branch
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)

    # 核心代码！！！！！！！！！！！！！！！！！！递归！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    for value in uniqueVals:
        # 求出剩余的标签label， L1 = L[:]   #L1为L的克隆，即另一个拷贝
        subLabels = labels[:]
        del (subLabels[bestFeat])
        # 遍历当前选择特征包含的所有属性值，在每个数据集划分上递归调用函数createTree()
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)###############splitDataSet真的分割了
    return myTree


if __name__ == "__main__":
    myDat, labels = createDataSet()

    # 在这个例子中，两种写法的效果一样，因为labels是List对象属于可变对象，是引用传递
    myTree = createTree(myDat, labels)

    print myTree
