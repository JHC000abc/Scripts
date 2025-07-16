# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: many_single.py
@time: 2023/11/29 17:26
@desc: 连续帧拆成单帧

"""

from sdk.temp.temp_supports import IsSolution


class Solution(IsSolution):
    """
    Solution
    """

    def __init__(self, **kwargs):
        """
        初始化函数
        :param kwargs: 字典类型的参数字典，包含可选的关键字参数
        """
        super(Solution, self).__init__()
        self.__dict__.update({k: v for k, v in [
            i for i in locals().values() if isinstance(i, dict)][0].items()})

    def process(self, **kwargs):
        """
        处理文件

        :param kwargs: 关键字参数
        :return: 无返回值
        """
        in_path = kwargs["in_path"]  # 输入文件路径
        save_path = kwargs["save_path"]  # 保存文件路径
        answer_list = kwargs["answer_list"]
        question_id = kwargs["question_id"]
        self.folder.create_folder(save_path)  # 创建保存文件的文件夹
        for file, name in self.get_file(in_path, status=True):
            out_lis = []
            print("开始处理:", file, name)  # 打印文件名和名称
            for args in self.read_line(file, _id=question_id):
                page_id = args["line"][args["headers"].index("页id")]

                for url, _uuid, results in zip(self.get_url_list(args), self.json.loads(args["line"][args["headers"].index("_uuid")]),
                                               self.get_answer_list(args, answer_list)):
                    # print(url, "2",results)
                    # print(_uuid)
                    out_lis.append([url, question_id, _uuid, page_id, self.json.dumps({"result": [results]}, indent=None)])

                # break
            headers = ["url", "题目id", "_uuid", "页id"] + answer_list
            save_file = self.folder.merge_path([save_path, "单帧_{}".format(name)])
            print("成功导出到:{}".format(save_file))
            self.save_result(save_file, out_lis, headers=headers)


if __name__ == '__main__':
    in_path = R"D:\Desktop\1"
    save_path = R"D:\Desktop\2\40765_result_20231225170814"
    answer_list = ["验收答案", "拟合答案", "终审答案", "审核答案", "质检答案"]
    answer_order = input("请输入答案顺序[用|分隔(默认:验收答案|拟合答案|终审答案|审核答案|质检答案)]:")
    _answer_list = answer_order.split("|")
    if len(_answer_list) > 1:
        for i in _answer_list:
            if i not in answer_list:
                print("输入的答案顺序有误")
                exit()
        answer_list = _answer_list

    print(answer_list)
    question_id = "2"
    e = Solution()
    e.process(in_path=in_path, save_path=save_path, answer_list=answer_list, question_id=question_id)
