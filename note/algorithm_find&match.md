查找与匹配
    1）std::find系列
        通用信息：
            通过不同条件，返回范围内满足条件的第一个迭代器

        find            值查找
        find_if         条件查找
        find_if_not     反向条件查找
        find_first_of   范围满足查找

        如：
        find_if_not(v.begin(), v.end(), [](int x){return x<30;}) 找出第一个>=30的
        find_first_of(v.begin(), v.end(),
            target.begin(), target.end()) 找出第一个区间值等于第二区间的第一满足

    2）std::search系列
        
