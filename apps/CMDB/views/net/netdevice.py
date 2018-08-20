# #! /usr/bin/env python
# # -*- coding: utf-8 -*-
#
# from CMDB.forms.net_forms import NetDeviceForm
# from models import NetDevice, Idc, NetGroup, ASSET_STATUS, ASSET_TYPE
# from django.shortcuts import render, HttpResponse
# from django.db.models import Q
# # from cmdb.api import get_object
# # from cmdb.api import pages, str2gb
# from utils import pages
# import csv
# import datetime
# from django.contrib.auth.decorators import login_required
#
#
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
#
#
# @login_required()
#
# def netasset(request):
#     temp_name = "netcmdb/netcmdb-header.html"
#     asset_find = []
#     idc_info = Idc.objects.all()
#     host_list = NetDevice.objects.all()
#     group_info = NetGroup.objects.all()
#     asset_types = ASSET_TYPE
#     asset_status = ASSET_STATUS
#     idc_name = request.GET.get('idc', '')
#     group_name = request.GET.get('group', '')
#     asset_type = request.GET.get('asset_type', '')
#     status = request.GET.get('status', '')
#     keyword = request.GET.get('keyword', '')
#     export = request.GET.get("export", '')
#     group_id = request.GET.get("group_id", '')
#     idc_id = request.GET.get("idc_id", '')
#     asset_id_all = request.GET.getlist("id", '')
#
#     if group_id:
#         group = NetGroup.objects.filter(id=group_id)
#         if group:
#             asset_find = NetDevice.objects.filter(group=group)
#     elif idc_id:
#         idc = Idc.objects.filter(id=idc_id)
#         if idc:
#             asset_find = NetDevice.objects.filter(idc=idc)
#     else:
#         asset_find = NetDevice.objects.all()
#     if idc_name:
#         asset_find = asset_find.filter(idc__name__contains=idc_name)
#     if group_name:
#         asset_find = asset_find.filter(group__name__contains=group_name)
#     if asset_type:
#         asset_find = asset_find.filter(asset_type__contains=asset_type)
#     if status:
#         asset_find = asset_find.filter(status__contains=status)
#     if keyword:
#         asset_find = asset_find.filter(
#             Q(hostname__contains=keyword) |
#             Q(in_band_ip__contains=keyword) |
#             Q(out_band_ip__contains=keyword) |
#             Q(in_net_ip__contains=keyword) |
#             Q(brand__contains=keyword) |
#             Q(sn__contains=keyword) |
#             Q(location__contains=keyword) |
#             Q(memo__contains=keyword))
#     if export:
#         response = create_asset_excel(export, asset_id_all)
#         return response
#     assets_list, p, assets, page_range, current_page, show_first, show_end = pages.pages(asset_find, request)
#     return render(request, 'CMDB/net/netdvice_full_list.html', locals())
#
#
#
# def str2gb(args):
#     """
#     :参数 args:
#     :返回: GB2312编码
#     """
#     return str(args).encode('gb2312')
#
#
# def create_asset_excel(export, asset_id_all):
#     if export == "true":
#         if asset_id_all:
#             asset_find = []
#             for asset_id in asset_id_all:
#                 asset_item = NetDevice.objects.filter(id=asset_id)
#                 if asset_item:
#                     asset_find.append(asset_item)
#             response = HttpResponse(content_type='text/csv')
#             now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
#             file_name = 'qwkg_cmdb_' + now + '.csv'
#             response['Content-Disposition'] = "attachment; filename="+file_name
#             writer = csv.writer(response)
#             writer.writerow([str2gb(u'主机名'), str2gb(u'IP地址'), str2gb(u'其它IP'), str2gb(u'主机组'),
#                              str2gb(u'资产编号'), str2gb(u'设备类型'), str2gb(u'设备状态'), str2gb(u'操作系统'),
#                              str2gb(u'设备厂商'), str2gb(u'CPU型号'), str2gb(u'CPU核数'), str2gb(u'内存大小'),
#                              str2gb(u'硬盘信息'), str2gb(u'SN号码'), str2gb(u'所在机房'), str2gb(u'所在位置'),
#                              str2gb(u'备注信息')])
#             for h in asset_find:
#                 if h.asset_type:
#                     at_num = int(h.asset_type)
#                     a_type = ASSET_TYPE[at_num-1][1]
#                 else:
#                     a_type = ""
#                 if h.status:
#                     at_as = int(h.status)
#                     a_status = ASSET_STATUS[at_as-1][1]
#                 else:
#                     a_status = ""
#                 writer.writerow([str2gb(h.hostname), h.ip, h.other_ip, str2gb(h.group), str2gb(h.asset_no),
#                                  str2gb(a_type), str2gb(a_status), str2gb(h.os), str2gb(h.vendor),
#                                  str2gb(h.cpu_model), str2gb(h.cpu_num), str2gb(h.memory), str2gb(h.disk),
#                                  str2gb(h.sn), str2gb(h.idc), str2gb(h.position), str2gb(h.memo)])
#             return response
#
#     if export == "all":
#         host = NetDevice.objects.all()
#         response = HttpResponse(content_type='text/csv')
#         now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
#         file_name = 'qwkg_cmdb_' + now + '.csv'
#         response['Content-Disposition'] = "attachment; filename=" + file_name
#         writer = csv.writer(response)
#         writer.writerow([str2gb('主机名'), str2gb('IP地址'), str2gb('其它IP'), str2gb('主机组'), str2gb('资产编号'),
#                          str2gb('设备类型'), str2gb('设备状态'), str2gb('操作系统'), str2gb('设备厂商'), str2gb('CPU型号'),
#                          str2gb('CPU核数'), str2gb('内存大小'), str2gb('硬盘信息'), str2gb('SN号码'), str2gb('所在机房'),
#                          str2gb('所在位置'), str2gb('备注信息')])
#         for h in host:
#             if h.asset_type:
#                 at_num = int(h.asset_type)
#                 a_type = ASSET_TYPE[at_num-1][1]
#             else:
#                 a_type = ""
#             if h.status:
#                 at_as = int(h.status)
#                 a_status = ASSET_STATUS[at_as-1][1]
#             else:
#                 a_status = ""
#             writer.writerow([str2gb(h.hostname), h.ip, h.other_ip, str2gb(h.group), str2gb(h.asset_no), str2gb(a_type),
#                              str2gb(a_status), str2gb(h.os), str2gb(h.vendor), str2gb(h.cpu_model), str2gb(h.cpu_num),
#                              str2gb(h.memory), str2gb(h.disk), str2gb(h.sn), str2gb(h.idc), str2gb(h.position),
#                              str2gb(h.memo)])
#         return response
#
#
# @login_required()
# def asset_add(request):
#     temp_name = "netcmdb/netcmdb-header.html"
#     if request.method == "POST":
#         a_form = NetDeviceForm(request.POST)
#         if a_form.is_valid():
#             a_form.save()
#             tips = u"增加成功！"
#             display_control = ""
#         else:
#             tips = u"增加失败！"
#             display_control = ""
#         return render(request, "CMDB/net/netdvice_add.html", locals())
#     else:
#         display_control = "none"
#         a_form = NetDeviceForm()
#         return render(request, "CMDB/net/netdvice_add.html", locals())
#
#
# @login_required()
# def asset_del(request):
#     asset_id = request.GET.get('id', '')
#     if asset_id:
#         NetDevice.objects.filter(id=asset_id).delete()
#
#     if request.method == 'POST':
#         asset_batch = request.GET.get('arg', '')
#         asset_id_all = str(request.POST.get('asset_id_all', ''))
#
#         if asset_batch:
#             for asset_id in asset_id_all.split(','):
#                 asset_item = NetDevice.objects.filter( id=asset_id)
#                 asset_item.delete()
#
#     return HttpResponse(u'删除成功')
#
#
# @login_required
# def asset_edit(request, ids):
#     #temp_name = "netcmdb/netcmdb-header.html"
#     status = 0
#     asset_types = ASSET_TYPE
#     obj = NetDevice.objects.filter( id=ids)
#
#     if request.method == 'POST':
#         af = NetDeviceForm(request.POST, instance=obj)
#         if af.is_valid():
#             af.save()
#             status = 1
#         else:
#             status = 2
#     else:
#         af = NetDeviceForm(instance=obj)
#
#     return render(request, 'CMDB/net/netdevice_edit.html', locals())