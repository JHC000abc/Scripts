# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     :归档数据格式化

"""

from sdk.temp.temp_supports import IsSolution
from sdk.utils.util_excel import ExcelProcess


class Solution(IsSolution):
    """

    """

    def __init__(self, **kwargs):
        super(Solution, self).__init__()
        self.__dict__.update({k: v for k, v in [
            i for i in locals().values() if isinstance(i, dict)][0].items()})
        self.excel = ExcelProcess()

        self.his = "111"
        self.status = False

    def make_map_from_excel(self, file):
        """
        合格数据map
        :return:
        """
        map = {}
        for args in self.excel.read_yield(file):
            url = args["line"][args["headers"].index("url")]
            if map.get(url):
                print("重复:{}".format(url))
            else:
                map[url] = 1
        return map

    def make_map_from_excel2(self, file):
        map = {}
        for args in self.read_line(file):
            url = args["line"][args["headers"].index("bos地址")]
            if map.get(url):
                print("重复:{}".format(url))
            else:
                map[url] = 1
        return map

    def make_map_from_txt(self, file):
        map = {}
        for args in self.read_line(file):
            answer = self.get_answer(args, answer_list=["单元判定结果", "质检答案", "审核答案", "拟合答案"])
            print("answer", answer)
            # print(args["line"])
            url = args["line"][2]
            if answer == "合格":
                map[url] = 1
        return map

    def format_export(self, file):
        """
        格式化读取phpmyadmin导出的数据
        :param file:
        :return:
        """
        for args in self.read_line(file):
            data = args["line"]
            # print(data)
            if data == [''] and "== 转存表中的数据" in self.his:
                self.status = True
                continue

            if self.status:
                out = data[0].split("|")
                # print("out",out)
                yield out
            self.his = data[0]

    def process(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        in_path = kwargs["in_path"]
        save_path = kwargs["save_path"]

        self.folder.create_folder(save_path)

        file_export = self.folder.merge_path([in_path, "1.jsonl"])

        # file_excel = self.folder.merge_path([in_path, "1.xlsx"])
        # _stand_map = self.make_map_from_excel(file_excel)

        file_excel = self.folder.merge_path([in_path, "stand.txt"])
        # _stand_map = self.make_map_from_excel2(file_excel)
        _stand_map = self.make_map_from_txt(file_excel)

        print(_stand_map)

        match_lis = []
        not_match_lis = []

        for _, url, id, task_id, status in self.format_export(file_export):
            print(url, id, task_id, status)
            if _stand_map.get(url) is None:
                print("匹配失败链接:{}".format(url))
                not_match_lis.append([id, task_id, "2"])
            else:
                match_lis.append([id, task_id, status])

        if match_lis:
            self.save_result(self.folder.merge_path(
                [save_path, "update_file.txt"]), data=match_lis)

        if not_match_lis:
            self.save_result(self.folder.merge_path(
                [save_path, "not_match.txt"]), data=not_match_lis)

    def process_export(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        in_path = kwargs["in_path"]
        save_path = kwargs["save_path"]

        self.folder.create_folder(save_path)

        file_export = self.folder.merge_path([in_path, "1.txt"])

        out_lis = []
        # for _, url, id, task_id, status in self.format_export(file_export):
        #     print(_, id, task_id, status)
        #     out_lis.append([id, task_id, status])

        for _, id, task_id, status in self.format_export(file_export):
            # print(_, id, task_id, status)
            out_lis.append([id, task_id, status])

        self.save_result(self.folder.merge_path(
            [save_path, "update_file.txt"]), data=out_lis)

    def match_urls(self, file_export, file_stand):
        url_stand_set = set()
        for args in self.read_line(file_stand):
            # print(args)
            url = args["line"][args["headers"].index("bos地址")]
            # answer_str = self.get_answer(args, answer_list=["审核答案", "质检答案","拟合答案"])
            # print(answer_str)
            url_stand_set.add(url)

        success_lis = []
        error_lis = []

        for args in self.read_line(file_export, headers=["", "url", "id", "task_id"], spliter="|"):
            url = args["line"][args["headers"].index("url")]
            id = args["line"][args["headers"].index("id")]
            task_id = args["line"][args["headers"].index("task_id")]
            if url in url_stand_set:
                print("success")
                success_lis.append([id, task_id, "1"])
            else:
                print("error")
                error_lis.append([id, task_id, "2"])

        if success_lis:
            self.save_result(self.folder.merge_path(
                [save_path, "update_file.txt"]), data=success_lis)
        if error_lis:
            self.save_result(self.folder.merge_path(
                [save_path, "not_match.txt"]), data=error_lis)

    def process_by_url(self, file_right, file_all):
        """

        :param file_right:合不合格文件
        :param file_all: 所有数据.csv
        :return:
        """
        right_set = set()
        failed_set = set()
        other_set = set()
        for args in self.read_line(file_right):
        # for args in self.excel.read_yield_xlsx_by_xlrd(file_right):
            # print(args)
            url = self.get_one_from_yield_args(args, "bos地址")
            status = self.get_one_from_yield_args(args, "最终审核结果")
            print(status,url)
            if status in ("合格", "通过"):
                right_set.add(url)
            elif status in ("不合格", "未通过"):
                failed_set.add(url)
            else:
                other_set.add("\t".join([url, status]))

        for args in self.csv.read_yield_csv(file_all, headers=["url", "id", "task_id", "_"]):
            # print(args)
            url = self.get_one_from_yield_args(args, "url")
            id = self.get_one_from_yield_args(args, "id")
            task_id = self.get_one_from_yield_args(args, "task_id")
            # print(url)
            if url in right_set:
                self.success_lis.append([id, task_id, "1"])
            elif url in failed_set:
                self.error_lis.append([id, task_id, "2"])


        save_path = R"D:\Desktop\6"
        if self.success_lis:
            print(f"合格:{len(self.success_lis)}")
            self.save_result(self.folder.merge_path([save_path, "update_file.txt"]), self.success_lis)
            self.success_lis = []

        if self.error_lis:
            print(f"不合格:{len(self.error_lis)}")
            self.save_result(self.folder.merge_path([save_path, "update_file_error.txt"]), self.error_lis)
            self.error_lis = []

        if other_set:
            print(f"未知：{len(other_set)}")
            self.save_result(self.folder.merge_path([save_path, "other.txt"]), list(other_set))
            other_set.clear()

    def process_page_answer(self, **kwargs):
        """

        SELECT id, task_id,  answer FROM ct_collection_page_answer WHERE task_id=5980 AND audit_stage!=6

        :param kwargs:
        :return:
        """
        self.in_path = kwargs["in_path"]
        self.save_path = kwargs["save_path"]
        self.folder.create_folder(self.save_path)
        for file, _name in self.get_file(self.in_path, status=True):
            for args in self.csv.read_yield_csv(file, headers=["id", "task_id", "answer"]):
                # print(args)
                ans = self.json.loads(self.get_one_from_yield_args(args, "answer"))
                id = self.get_one_from_yield_args(args, "id")
                task_id = self.get_one_from_yield_args(args, "task_id")
                # print(ans)
                for k, v in ans.items():
                    url = v["answer"][0]["url"]
                    if "8d624153-929f-4280-b52a-084304ef54d9_2024-09-05-06-53-16-209.wav" in url:
                        print(url)
                # break
            #     tmp_map = {}
            #     for k,v in ans.items():
            #         # print(k)
            #         tmp_map[str(k)] = 2
            #     tmp_map  = dict(sorted(tmp_map.items(), key=lambda x: int(x[0])))
            #     self.success_lis.append([id,task_id,self.json.dumps(tmp_map,indent=None)])
            # print(len(self.success_lis))
            # self.save_result(self.folder.merge_path([self.save_path,'update_file.txt']),self.success_lis)
            # self.success_lis = []
            # break

    def process_page_answer_2(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        self.in_path = kwargs["in_path"]
        self.save_path = kwargs["save_path"]
        self.folder.create_folder(self.save_path)
        for file, _name in self.get_file(self.in_path, status=True):
            for args in self.excel.read_yield_xlsx_by_xlrd(file):
                print(args)
                id = self.get_one_from_yield_args(args, "collection_data_answer_id")
                task_id = "5979"
                ans = {}
                status = self.get_one_from_yield_args(args, "拟合答案")
                if status == "不合格":
                    tag = 2
                else:
                    tag = 1
                for i in range(1, 11):
                    ans[f"{i}"] = tag
                # print(ans)
                self.success_lis.append([id, task_id, self.json.dumps(ans, indent=None)])

                # break
        self.save_result(self.folder.merge_path([self.save_path, 'update_file.txt']), self.success_lis)
        self.success_lis = []


if __name__ == '__main__':
    in_path = R"D:\Desktop\5"
    save_path = R"D:\Desktop\6"
    e = Solution()
    # 正确率相关  unit 表  accuracy_rate *100 不保留小数

    # 直接导出数据处理
    e.process_export(in_path=in_path, save_path=save_path)

    # e.process_by_url(file_right=R"C:\Users\v_jiaohaicheng\Downloads\智源小时583.txt",
    #                  file_all=R"C:\Users\v_jiaohaicheng\Downloads\ct_collection_item_04 (1).csv")

    # e.process_by_url(file_right=R"C:\Users\v_jiaohaicheng\Downloads\灵初32小时.txt",
    #                  file_all=R"C:\Users\v_jiaohaicheng\Downloads\ct_collection_item_09 (1)csv")

    # e.process_page_answer(in_path=in_path,save_path=save_path)
    # e.process_page_answer_2(in_path=in_path,save_path=save_path)
