#!/usr/bin/env python3
import re
import xlsxwriter
import pandas as pd
from collections import defaultdict


def output_movie_excel(movie_list, excel_path, sheet_name="电影资料馆片单"):

    # 按照 date 进行处理
    date2movies = defaultdict(list)
    for movie_item in movie_list:
        date_key = movie_item["sorted_date"]
        date2movies[date_key].append(movie_item)
    date_list = list(date2movies.keys())
    date_list = sorted(date_list)
    start_date = date2movies[date_list[0]][0]["date"]
    end_date = date2movies[date_list[-1]][0]["date"]

    workbook = xlsxwriter.Workbook(excel_path)
    worksheet = workbook.add_worksheet(sheet_name)

    top_date_format = workbook.add_format({"bg_color": "#DE8345", "border": 3, "border_color": "white",
                                           "text_wrap": True, "align": "center", "valign": "vcenter",
                                           "font_name": "Times New Roman", "font_color": "white"})
    top_format = workbook.add_format({"bg_color": "#DE8345", "border": 3, "border_color": "white",
                                      "text_wrap": True, "valign": "vcenter"})
    english_font_format = workbook.add_format({"font_name": "Times New Roman", "font_color": "white"})
    chinese_font_format = workbook.add_format({"font_name": "宋体", "font_color": "white"})
    english_big_font_format = workbook.add_format({"font_name": "Times New Roman", "font_color": "white", "font_size": 13})
    chinese_big_font_format = workbook.add_format({"font_name": "宋体", "font_color": "white", "font_size": 13})
    english_small_font_format = workbook.add_format({"font_name": "Times New Roman", "font_color": "white", "font_size": 9})
    chinese_small_font_format = workbook.add_format({"font_name": "宋体", "font_color": "white", "font_size": 9})

    title_format = workbook.add_format({"bg_color": "#818080", "border": 3, "border_color": "white",
                                        "text_wrap": True, "align": "center", "valign": "vcenter",
                                        "font_name": "宋体", "font_color": "white", "font_size": 10})

    content_date_format = workbook.add_format({"bg_color": "#818080", "border": 3, "border_color": "white",
                                               "text_wrap": True, "align": "center", "valign": "vcenter",
                                               "font_name": "Times New Roman", "font_color": "white"})
    content_format = workbook.add_format({"bg_color": "#F2F2F2", "border": 3, "border_color": "white",
                                          "align": "center", "valign": "vcenter"})
    content_chinese_format = workbook.add_format({"bg_color": "#F2F2F2", "border": 3, "border_color": "white",
                                                  "align": "center", "valign": "vcenter",
                                                  "font_name": "宋体", "font_color": "black"})
    content_english_format = workbook.add_format({"bg_color": "#F2F2F2", "border": 3, "border_color": "white",
                                                  "align": "center", "valign": "vcenter",
                                                  "font_name": "Times New Roman", "font_color": "black"})
    content_chinese_font_format = workbook.add_format({"font_name": "宋体", "font_color": "black"})
    content_english_font_format = workbook.add_format({"font_name": "Times New Roman", "font_color": "black"})
    content_info_title_english_format = workbook.add_format({"font_name": "Times New Roman", "font_color": "gray"})
    content_info_title_chinese_format = workbook.add_format({"font_name": "宋体", "font_color": "black"})
    content_info_title_format = workbook.add_format({"bg_color": "#F2F2F2", "top": 3, "left": 3, "right": 3, "border_color": "white",
                                                     "align": "left", "valign": "vcenter"})
    content_info_year_format = workbook.add_format({"bg_color": "#F2F2F2", "left": 3, "right": 3, "border_color": "white",
                                                    "align": "left", "valign": "vcenter", "font_name": "Times New Roman"})
    content_info_country_format = workbook.add_format({"bg_color": "#F2F2F2", "bottom": 3, "left": 3, "right": 3, "border_color": "white",
                                                       "align": "right", "valign": "vcenter", "font_color": "gray"})

    # 进行首行的设置
    worksheet.set_row(0, 60)  # 设置第一行行高 60
    worksheet.write("A1", f"{start_date}\n-{end_date}", top_date_format)
    cinema_list = list(set([ x['theater'] for x in movie_list]))
    if '小西天1号厅' in cinema_list:
        cfa_titles = [chinese_big_font_format, "中国电影资料馆", english_big_font_format, " CFA\n",
                     chinese_font_format, "日常放映场次表", english_font_format, " Screening Schedule"]
        loc_titles = [chinese_small_font_format, "小西天影院|海淀区文慧园路", english_small_font_format, "3",
                      chinese_small_font_format, "号\n百子湾影院|朝阳区百子湾南二路", english_small_font_format, "2",
                      chinese_small_font_format, "号\n网售平台|淘票票/中国电影资料馆", english_small_font_format, "APP"]
    else:
        cfa_titles = [chinese_big_font_format, "中国电影资料馆江南分馆", english_big_font_format, " CFA JIANGNAN CENTER\n",
                     chinese_font_format, "日常放映场次表", english_font_format, " Screening Schedule"]
        loc_titles = [chinese_small_font_format, "江南分馆影院|苏州市姑苏区景德路", english_small_font_format, "523",
                      chinese_small_font_format, "号(长船湾青年码头东岸)\n网售平台|淘票票/中国电影资料馆", english_small_font_format, "APP"]
    worksheet.merge_range("B1:C1", "", top_format)
    worksheet.write_rich_string("B1", *cfa_titles, top_format)
    worksheet.merge_range("D1:F1", "", top_date_format)
    worksheet.write_rich_string("D1", *loc_titles, top_format)

    # 进行标题相关设置
    col_date = 0
    col_time = 1
    col_info = 2
    col_duration = 3
    col_theater = 4
    col_price = 5

    worksheet.write(1, col_date, "日期", title_format)
    worksheet.write(1, col_time, "放映时间", title_format)
    worksheet.write(1, col_info, "影片信息", title_format)
    worksheet.write(1, col_duration, "时长", title_format)
    worksheet.write(1, col_theater, "影厅", title_format)
    worksheet.write(1, col_price, "票价", title_format)

    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('C:C', 48)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 15)
    worksheet.set_column('F:F', 10)

    # 进行内容相关设置
    theater_order = ["小西天1号厅", "小西天2号厅", "小西天3号厅", "小西天4号厅", "百子湾厅", "江南分馆1号厅", "江南分馆2号厅", "江南分馆3号厅", "江南分馆4号厅"]
    theater_order_map = {theater: index for index, theater in enumerate(theater_order)}

    row_idx = 1
    for date_key in date_list:
        movie_items = date2movies[date_key]
        movie_items = sorted(movie_items, key=lambda x: (theater_order_map.get(x["theater"], 1), x["time"]))  # 按影院\放映时间排序

        date_start_row_id = row_idx + 2
        for movie_item in movie_items:
            movie_time = movie_item["time"]
            chinese_title = movie_item["chinese_title"]
            english_title = movie_item["english_title"]
            year = movie_item["year"]
            director = movie_item["director"]
            country = movie_item["country"]
            duration = movie_item["duration"]
            theater = movie_item["theater"]
            price = movie_item["price"]

            row_idx += 1
            start_row_id = row_idx + 1
            info_title_list = [content_info_title_chinese_format, chinese_title, content_info_title_english_format, f"    {english_title}"]
            worksheet.write_rich_string(row_idx, col_info, *info_title_list, content_info_title_format)
            row_idx += 1
            worksheet.write(row_idx, col_info, year, content_info_year_format)
            row_idx += 1
            worksheet.write(row_idx, col_info, f"{country}|{director}", content_info_country_format)
            end_row_id = row_idx + 1

            worksheet.merge_range(f"B{start_row_id}:B{end_row_id}", movie_time, content_english_format)
            worksheet.merge_range(f"D{start_row_id}:D{end_row_id}", f"{duration}'", content_english_format)
            worksheet.merge_range(f"E{start_row_id}:E{end_row_id}", theater, content_chinese_format)
            # price_list = [content_english_font_format, f"{price}", content_chinese_font_format, "元"]
            # worksheet.merge_range(f"F{start_row_id}:F{end_row_id}", "", content_chinese_format)
            # worksheet.write_rich_string(f"F{start_row_id}", *price_list, content_format)
            worksheet.merge_range(f"F{start_row_id}:F{end_row_id}", f"{price}元", content_english_format)

        date_end_row_id = row_idx + 1
        output_date = f"{movie_items[0]['date']}\n（{movie_items[0]['week']}）"
        worksheet.merge_range(f"A{date_start_row_id}:A{date_end_row_id}", output_date, content_date_format)

    workbook.close()


def test_v1():
    excel_path = "./240224电影资料馆片单排版测试.xlsx"

    movie_item1 = {"date": "12.16", "week": "六", "time": "11:00", "chinese_title": "晒后假日", "english_title": "Aftersun",
                   "year": 2022, "director": "夏洛特.威尔斯", "country": "美国/英国", "duration": 101, "theater": "小西天1号厅",
                   "price": 60}
    movie_item2 = movie_item1.copy()
    movie_item2["chinese_title"] = "晒后假日2"
    movie_item3 = movie_item1.copy()
    movie_item3["date"] = "12.17"
    movie_item3["week"] = "日"
    movie_item3["chinese_title"] = "晒后假日3"
    movie_item4 = movie_item3.copy()
    movie_item4["chinese_title"] = "晒后假日4"
    movie_item5 = movie_item3.copy()
    movie_item5["chinese_title"] = "晒后假日5"
    movie_list = [movie_item1, movie_item2, movie_item3, movie_item4, movie_item5]

    output_movie_excel(movie_list, excel_path)


def parse_movie_excel(excel_path, cinema):
    table = pd.read_excel(excel_path, sheet_name="排片表", keep_default_na=False)
    data_list = table.to_dict("records")
    movie_list = []
    for data_item in data_list:
        if data_item["theater"] in cinema:
            date = data_item["date"]
            match = re.match(r"(\d{2})月(\d{2})日", date)
            if match:
                month, day = match.groups()
                month = int(month)
                day = int(day)
                data_item["sorted_date"] = f"{month:02}.{day:02}"
                data_item["date"] = f"{month}.{day}"
                data_item["month"] = month
                data_item["day"] = day
            week = data_item["week"]
            week = week.lstrip("周")
            data_item["week"] = week
    
            movie_time = data_item["time"]
            movie_start_time = movie_time.split("-")[0]
            data_item["time"] = movie_start_time
    
            theater = data_item["theater"]
            movie_hall = data_item["movieHall"]
            theater_name = f"{theater}{movie_hall}"
            if theater in ["百子湾艺术影院"]:
                theater_name = "百子湾厅"
            elif theater in ["小西天艺术影院"]:
                theater_name = "小西天"
                theater_name = f"{theater_name}{movie_hall}"
            elif theater in ["江南分馆影院"]:
                theater_name = "江南分馆"
                theater_name = f"{theater_name}{movie_hall}"
            data_item["theater"] = theater_name
    
            film = data_item["film"]
            data_item["chinese_title"] = film
            data_item["english_title"] = ""
            fare = data_item["fare"]
            data_item["price"] = int(fare)
    
            movie_list.append(data_item)
            # print(data_item.keys())
            # for k, v in data_item.items():
            #     print(k, v)
            # break
    
    #return data_list
    return movie_list


def test_v2():
    input_excel_path = "./zlg_schedule.xlsx"
    output_excel_path = "./中国电影资料馆片单.xlsx"
    output_excel_path_jnfg = "./中国电影资料馆片单_江南分馆.xlsx"
    try:
        movie_list = parse_movie_excel(input_excel_path, ["小西天艺术影院", "百子湾艺术影院"])
        output_movie_excel(movie_list, output_excel_path)
    except Exception as e:
        pass
    try:
        movie_list_jnfg = parse_movie_excel(input_excel_path, ['江南分馆影院'])
        output_movie_excel(movie_list_jnfg, output_excel_path_jnfg)
    except Exception as e:
        pass


if __name__ == '__main__':
    # test_v1()
    test_v2()


