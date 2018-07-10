from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from random import seed, sample
from ichingdb.models import Consultation, LineChanges
from datetime import datetime

def index(request):
    consultation_list = reversed(Consultation.objects.all())
    return render(request, 'ichingdb/index.html', {'consultation_list': consultation_list})

def reading(request, cid):
    simple_query = "SELECT DISTINCT consultation_id, query, lc.hexagram AS initial, h.name AS initial_name, h.description AS initial_desc, h.gnostic AS initial_gnostic, pair.hexagram2 AS mirror, h2.name AS mirror_name, h2.description AS mirror_desc, h2.gnostic AS mirror_gnostic, hidden.hexagram_id AS hidden, hidden.name AS h_name, hidden.description AS h_desc, hidden.gnostic AS h_gnostic, shadow.hexagram_id AS shadow, shadow.name AS s_name, shadow.description AS s_desc, shadow.gnostic AS s_gnostic, notes, conclusion FROM consultation AS C JOIN line_changes AS lc USING (line_1 , line_2 , line_3 , line_4 , line_5 , line_6) JOIN hexagram AS h ON h.hexagram_id = lc.hexagram, hexagram AS h2, pair, line_changes AS lch, hexagram AS hidden, hexagram AS shadow WHERE lc.chng_1 = 0 AND lc.chng_2 = 0 AND lc.chng_3 = 0 AND lc.chng_4 = 0 AND lc.chng_5 = 0 AND lc.chng_6 = 0 AND pair.hexagram1_id = lc.hexagram AND h2.hexagram_id = pair.hexagram2 AND lch.line_1 = C.line_2 AND lch.line_2 = C.line_3 AND lch.line_3 = C.line_4 AND lch.line_4 = C.line_3 AND lch.line_5 = C.line_4 AND lch.line_6 = C.line_5 AND lch.chng_1 = 0 AND lch.chng_2 = 0 AND lch.chng_3 = 0 AND lch.chng_4 = 0 AND lch.chng_5 = 0 AND lch.chng_6 = 0 AND hidden.hexagram_id = lch.hexagram AND shadow.hexagram_id = 65 - h.hexagram_id AND consultation_id = %d;" % cid
    line_query = "SELECT C.consultation_id, lc2.hexagram AS result, h1.name AS result_name, h1.description AS result_desc, h1.gnostic AS result_gnostic, hl.h_line_position AS line, hlp.name AS line_name, hlp.meaning AS line_desc, hl.related_hexagram AS context, h3.name AS context_name, h3.description AS context_desc, h3.gnostic AS context_gnostic, hl.translation AS line_trans, hl.commentary AS line_comm, hl2.h_line_position AS m_line, hlp2.name AS m_line_name, hlp2.meaning AS m_line_desc, hl2.related_hexagram AS m_context, h4.name AS m_context_name, h4.description AS m_context_desc, h4.gnostic AS m_context_gnostic, hl2.translation AS m_trans, hl2.commentary AS m_comm, innerop.hexagram_id AS innerop, innerop.name AS i_name, innerop.description AS i_desc, innerop.gnostic AS i_gnostic, outerop.hexagram_id AS outerop, outerop.name AS o_name, outerop.description AS o_desc, outerop.gnostic AS o_gnostic FROM consultation AS C JOIN line_changes AS lc USING (line_1 , line_2 , line_3 , line_4 , line_5 , line_6) JOIN line_changes AS lc2 USING (line_1 , line_2 , line_3 , line_4 , line_5 , line_6) JOIN hexagram AS h ON h.hexagram_id = lc.hexagram JOIN hexagram AS h1 ON h1.hexagram_id = lc2.hexagram, hexagram AS h2, pair, hexagram_line AS hl, hexagram AS h3, hexagram_line AS hl2, hexagram AS h4, h_line_position AS hlp, h_line_position AS hlp2, line_changes AS lci, hexagram AS innerop, line_changes AS lco, hexagram AS outerop WHERE lc.chng_1 = 0 AND lc.chng_2 = 0 AND lc.chng_3 = 0 AND lc.chng_4 = 0 AND lc.chng_5 = 0 AND lc.chng_6 = 0 AND lc2.chng_1 = C.chng_1 AND lc2.chng_2 = C.chng_2 AND lc2.chng_3 = C.chng_3 AND lc2.chng_4 = C.chng_4 AND lc2.chng_5 = C.chng_5 AND lc2.chng_6 = C.chng_6 AND hl.hexagram = lc.hexagram AND hl.related_hexagram = h3.hexagram_id AND ((hl.h_line_position = 1 AND lc2.chng_1 = 1) OR (hl.h_line_position = 2 AND lc2.chng_2 = 1) OR (hl.h_line_position = 3 AND lc2.chng_3 = 1) OR (hl.h_line_position = 4 AND lc2.chng_4 = 1) OR (hl.h_line_position = 5 AND lc2.chng_5 = 1) OR (hl.h_line_position = 6 AND lc2.chng_6 = 1)) AND pair.hexagram1_id = lc.hexagram AND hl2.hexagram = pair.hexagram2 AND hl2.h_line_position = 7 - hl.h_line_position AND h4.hexagram_id = hl2.related_hexagram AND h2.hexagram_id = pair.hexagram2 AND hl.h_line_position = hlp.h_line_position_id AND hl2.h_line_position = hlp2.h_line_position_id AND lci.line_1 = MOD(C.chng_1 + 1, 2) AND lci.line_2 = MOD(C.chng_2 + 1, 2) AND lci.line_3 = MOD(C.chng_3 + 1, 2) AND lci.line_4 = MOD(C.chng_4 + 1, 2) AND lci.line_5 = MOD(C.chng_5 + 1, 2) AND lci.line_6 = MOD(C.chng_6 + 1, 2) AND lci.chng_1 = 0 AND lci.chng_2 = 0 AND lci.chng_3 = 0 AND lci.chng_4 = 0 AND lci.chng_5 = 0 AND lci.chng_6 = 0 AND innerop.hexagram_id = lci.hexagram AND lco.line_1 = C.chng_1 AND lco.line_2 = C.chng_2 AND lco.line_3 = C.chng_3 AND lco.line_4 = C.chng_4 AND lco.line_5 = C.chng_5 AND lco.line_6 = C.chng_6 AND lco.chng_1 = 0 AND lco.chng_2 = 0 AND lco.chng_3 = 0 AND lco.chng_4 = 0 AND lco.chng_5 = 0 AND lco.chng_6 = 0 AND outerop.hexagram_id = lco.hexagram AND consultation_id = %d;" % cid
    c = get_object_or_404(Consultation, pk=cid)
    simple_result = Consultation.objects.raw(simple_query)
    if c.chng_1 == 1 or c.chng_2 == 1 or c.chng_3 == 1 or c.chng_4 == 1 or c.chng_5 == 1 or c.chng_6 == 1:
        line_result = Consultation.objects.raw(line_query)
        return render(request, 'ichingdb/reading.html', {'cid': cid, 'simple_result': simple_result,'line_result': line_result})
    return render(request, 'ichingdb/reading.html', {'cid': cid, 'simple_result': simple_result,'line_result': False})

def reading2(request, hid, rid):
    simple_query = "SELECT DISTINCT lc.line_changes_id, 0, '', h.hexagram_id AS initial, h.name AS initial_name, h.description AS initial_desc, h.gnostic AS initial_gnostic, pair.hexagram2 AS mirror, h2.name AS mirror_name, h2.description AS mirror_desc, h2.gnostic AS mirror_gnostic, hidden.hexagram_id AS hidden, hidden.name AS h_name, hidden.description AS h_desc, hidden.gnostic AS h_gnostic, shadow.hexagram_id AS shadow, shadow.name AS s_name, shadow.description AS s_desc, shadow.gnostic AS s_gnostic, '', '' FROM hexagram AS h, hexagram AS h2, pair, line_changes AS lc, line_changes AS lcr, line_changes AS lch, hexagram AS hidden, hexagram AS shadow WHERE pair.hexagram1_id = h.hexagram_id AND h2.hexagram_id = pair.hexagram2 AND lc.chng_1 = 0 AND lc.chng_2 = 0 AND lc.chng_3 = 0 AND lc.chng_4 = 0 AND lc.chng_5 = 0 AND lc.chng_6 = 0 AND lc.hexagram = h.hexagram_id AND lch.line_1 = lc.line_2 AND lch.line_2 = lc.line_3 AND lch.line_3 = lc.line_4 AND lch.line_4 = lc.line_3 AND lch.line_5 = lc.line_4 AND lch.line_6 = lc.line_5 AND lch.chng_1 = 0 AND lch.chng_2 = 0 AND lch.chng_3 = 0 AND lch.chng_4 = 0 AND lch.chng_5 = 0 AND lch.chng_6 = 0 AND hidden.hexagram_id = lch.hexagram AND shadow.hexagram_id = 65 - h.hexagram_id AND h.hexagram_id = %d;" % hid
    line_query = "SELECT DISTINCT lc.line_changes_id, lcr.hexagram AS result, rel.name AS result_name, rel.description AS result_desc, rel.gnostic AS result_gnostic, hl.h_line_position AS line, hlp.name AS line_name, hlp.meaning AS line_desc, hl.related_hexagram AS context, h3.name AS context_name, h3.description AS context_desc, h3.gnostic AS context_gnostic, hl.translation AS line_trans, hl.commentary AS line_comm, hl2.h_line_position AS m_line, hlp2.name AS m_line_name, hlp2.meaning AS m_line_desc, hl2.related_hexagram AS m_context, h4.name AS m_context_name, h4.description AS m_context_desc, h4.gnostic AS m_context_gnostic, hl2.translation AS m_trans, hl2.commentary AS m_comm, innerop.hexagram_id AS innerop, innerop.name AS i_name, innerop.description AS i_desc, innerop.gnostic AS i_gnostic, outerop.hexagram_id AS outerop, outerop.name AS o_name, outerop.description AS o_desc, outerop.gnostic AS o_gnostic FROM hexagram AS h, hexagram AS rel, line_changes AS lc, line_changes AS lcr, hexagram AS h2, pair, hexagram_line AS hl, hexagram AS h3, hexagram_line AS hl2, hexagram AS h4, h_line_position AS hlp, h_line_position AS hlp2, line_changes AS lci, hexagram AS innerop, line_changes AS lco, hexagram AS outerop WHERE lc.chng_1 = 0 AND lc.chng_2 = 0 AND lc.chng_3 = 0 AND lc.chng_4 = 0 AND lc.chng_5 = 0 AND lc.chng_6 = 0 AND lc.hexagram = h.hexagram_id AND lc.line_1 = lcr.line_1 AND lc.line_2 = lcr.line_2 AND lc.line_3 = lcr.line_3 AND lc.line_4 = lcr.line_4 AND lc.line_5 = lcr.line_5 AND lc.line_6 = lcr.line_6 AND lcr.hexagram = rel.hexagram_id AND hl.hexagram = lc.hexagram AND hl.related_hexagram = h3.hexagram_id AND ((hl.h_line_position = 1 AND lcr.chng_1 = 1) OR (hl.h_line_position = 2 AND lcr.chng_2 = 1) OR (hl.h_line_position = 3 AND lcr.chng_3 = 1) OR (hl.h_line_position = 4 AND lcr.chng_4 = 1) OR (hl.h_line_position = 5 AND lcr.chng_5 = 1) OR (hl.h_line_position = 6 AND lcr.chng_6 = 1)) AND pair.hexagram1_id = lc.hexagram AND hl2.hexagram = pair.hexagram2 AND hl2.h_line_position = 7 - hl.h_line_position AND h4.hexagram_id = hl2.related_hexagram AND h2.hexagram_id = pair.hexagram2 AND hl.h_line_position = hlp.h_line_position_id AND hl2.h_line_position = hlp2.h_line_position_id AND lci.line_1 = MOD(lcr.chng_1 + 1, 2) AND lci.line_2 = MOD(lcr.chng_2 + 1, 2) AND lci.line_3 = MOD(lcr.chng_3 + 1, 2) AND lci.line_4 = MOD(lcr.chng_4 + 1, 2) AND lci.line_5 = MOD(lcr.chng_5 + 1, 2) AND lci.line_6 = MOD(lcr.chng_6 + 1, 2) AND lci.chng_1 = 0 AND lci.chng_2 = 0 AND lci.chng_3 = 0 AND lci.chng_4 = 0 AND lci.chng_5 = 0 AND lci.chng_6 = 0 AND innerop.hexagram_id = lci.hexagram AND lco.line_1 = lcr.chng_1 AND lco.line_2 = lcr.chng_2 AND lco.line_3 = lcr.chng_3 AND lco.line_4 = lcr.chng_4 AND lco.line_5 = lcr.chng_5 AND lco.line_6 = lcr.chng_6 AND lco.chng_1 = 0 AND lco.chng_2 = 0 AND lco.chng_3 = 0 AND lco.chng_4 = 0 AND lco.chng_5 = 0 AND lco.chng_6 = 0 AND outerop.hexagram_id = lco.hexagram AND h.hexagram_id = %d AND rel.hexagram_id = %d;" % (hid, rid)
    simple_result = LineChanges.objects.raw(simple_query)
    if hid != rid:
        line_result = LineChanges.objects.raw(line_query)
        return render(request, 'ichingdb/reading.html', {'cid': 0, 'simple_result': simple_result,'line_result': line_result})
    return render(request, 'ichingdb/reading.html', {'cid': 0, 'simple_result': simple_result,'line_result': False})

def explore(request):
    if request.method == 'POST':
        l1 = request.POST.get('l1', None)
        l2 = request.POST.get('l2', None)
        l3 = request.POST.get('l3', None)
        l4 = request.POST.get('l4', None)
        l5 = request.POST.get('l5', None)
        l6 = request.POST.get('l6', None)
        c1 = request.POST.get('c1', None)
        c2 = request.POST.get('c2', None)
        c3 = request.POST.get('c3', None)
        c4 = request.POST.get('c4', None)
        c5 = request.POST.get('c5', None)
        c6 = request.POST.get('c6', None)
        explore_query = "select lc.line_changes_id, h.hexagram_id as h_id, h.name as h_name, rel.hexagram_id as r_id, rel.name as r_name, ' ', hl6.line as l6, hl5.line as l5, hl4.line as l4, hl3.line as l3, hl2.line as l2, hl1.line as l1, ' ', lc.chng_6 as c6, lc.chng_5 as c5, lc.chng_4 as c4, lc.chng_3 as c3, lc.chng_2 as c2, lc.chng_1 as c1 from hexagram as h, hexagram_line as hl1, hexagram_line as hl2, hexagram_line as hl3, hexagram_line as hl4, hexagram_line as hl5, hexagram_line as hl6, line_changes as lc, hexagram as rel where h.hexagram_id = hl1.hexagram and h.hexagram_id = hl2.hexagram and h.hexagram_id = hl3.hexagram and h.hexagram_id = hl4.hexagram and h.hexagram_id = hl5.hexagram and h.hexagram_id = hl6.hexagram and hl6.h_line_position=6 and hl5.h_line_position=5 and hl4.h_line_position=4 and hl3.h_line_position=3 and hl2.h_line_position=2 and hl1.h_line_position=1 and lc.line_6 = hl6.line and lc.line_5 = hl5.line and lc.line_4 = hl4.line and lc.line_3 = hl3.line and lc.line_2 = hl2.line and lc.line_1 = hl1.line and rel.hexagram_id = lc.hexagram and hl6.line in (%s) and hl5.line in (%s) and hl4.line in (%s) and hl3.line in (%s) and hl2.line in (%s) and hl1.line in (%s) and lc.chng_6 in (%s) and lc.chng_5 in (%s) and lc.chng_4 in (%s) and lc.chng_3 in (%s) and lc.chng_2 in (%s) and lc.chng_1 in (%s) order by l6, l5, l4, l3, l2, l1, c6, c5, c4, c3, c2, c1;" % (l6, l5, l4, l3, l2, l1, c6, c5, c4, c3, c2, c1)
        explore_result = LineChanges.objects.raw(explore_query)
        html=""
        length = 0
        if explore_result:
            for i, r in enumerate(explore_result):
                html += "<tr><td>%d</td><td>%d %s</td><td>%d%d%d%d%d%d</td><td>%d%d%d%d%d%d</td><td>%d %s</td><td><a href=\"/ichingdb/%d/%d/\">Reading</a></td></tr>" % (i+1, r.h_id, r.h_name, r.l6, r.l5, r.l4, r.l3, r.l2, r.l1, r.c6, r.c5, r.c4, r.c3, r.c2, r.c1, r.r_id, r.r_name, r.h_id, r.r_id)
                length = i+1
        header="<!DOCTYPE html><html><head><style>table, th, td {border: 1px solid black; border-collapse: collapse; padding: 5px;}</style></head><body><h1>Pattern</h1><table><tr><th>Lines</th><th>Changes</th></tr><tr><td>%s</td><td>%s</td></tr><tr><td>%s</td><td>%s</td></tr><tr><td>%s</td><td>%s</td></tr><tr><td>%s</td><td>%s</td></tr><tr><td>%s</td><td>%s</td></tr><tr><td>%s</td><td>%s</td></tr></table><h1>%d Matches:</h1><table><tr><th>idx</th><th>Initial</th><th>Lines</th><th>Changes</th><th>Related</th><th>Link</th></tr>" % (l6, c6, l5, c5, l4, c4, l3, c3, l2, c2, l1, c1, length)
        footer = "</table></body></html>"
        return HttpResponse(header + html + footer)
    else:
        return render(request, 'ichingdb/explore.html')

def related(request):
    if request.method == 'POST':
        initial = int(request.POST.get('initial', None))
        levels = request.POST.get('levels', None)
        related_query = "SELECT DISTINCT lc.line_changes_id, h.hexagram_id AS h_id, h.name AS h_name, ' ', lc.line_6 as l6, lc.line_5 as l5, lc.line_4 as l4, lc.line_3 as l3, lc.line_2 as l2, lc.line_1 as l1, ' ', lcr.chng_6 as c6, lcr.chng_5 as c5, lcr.chng_4 as c4, lcr.chng_3 as c3, lcr.chng_2 as c2, lcr.chng_1 as c1, ' ', lcr.chng_6 + lcr.chng_5 + lcr.chng_4 + lcr.chng_3 + lcr.chng_2 + lcr.chng_1 AS len, ' ', rel.hexagram_id AS r_id, rel.name AS r_name FROM hexagram AS h, hexagram AS rel, line_changes AS lc, line_changes AS lcr WHERE lc.chng_1 = 0 AND lc.chng_2 = 0 AND lc.chng_3 = 0 AND lc.chng_4 = 0 AND lc.chng_5 = 0 AND lc.chng_6 = 0 AND lc.hexagram = h.hexagram_id AND lc.line_1 = lcr.line_1 AND lc.line_2 = lcr.line_2 AND lc.line_3 = lcr.line_3 AND lc.line_4 = lcr.line_4 AND lc.line_5 = lcr.line_5 AND lc.line_6 = lcr.line_6 AND lcr.chng_6 + lcr.chng_5 + lcr.chng_4 + lcr.chng_3 + lcr.chng_2 + lcr.chng_1 in (%s) AND lcr.hexagram = rel.hexagram_id AND h.hexagram_id = %d order by len, l6, l5, l4, l3, l2, l1, c6, c5, c4, c3, c2, c1;" % (levels, initial)
        related_result = LineChanges.objects.raw(related_query)
        html=""
        length = 0
        if related_result:
            for i, r in enumerate(related_result):
                html += "<tr><td>%d</td><td>%d %s</td><td>%d%d%d%d%d%d</td><td>%d%d%d%d%d%d</td><td>%d %s</td><td>%d</td><td><a href=\"/ichingdb/%d/%d/\">Reading</a></td></tr>" % (i+1, r.h_id, r.h_name, r.l6, r.l5, r.l4, r.l3, r.l2, r.l1, r.c6, r.c5, r.c4, r.c3, r.c2, r.c1, r.r_id, r.r_name, r.len, r.h_id, r.r_id)
                length = i+1
        header="<!DOCTYPE html><html><head><style>table, th, td {border: 1px solid black; border-collapse: collapse; padding: 5px;}</style></head><body><h1>Inputs</h1><table><tr><th>Initial</th><th>Levels</th></tr><tr><td>%s</td><td>%s</td></tr></table><h1>%d Matches:</h1><table><tr><th>idx</th><th>Initial</th><th>Lines</th><th>Changes</th><th>Related</th><th>Len</th><th>Link</th></tr>" % (initial, levels, length)
        footer = "</table></body></html>"
        return HttpResponse(header + html + footer)
    else:
        return render(request, 'ichingdb/related.html')

def paths(request):
    if request.method == 'POST':
        steps = request.POST.get('steps', None)
        initial = int(request.POST.get('initial', None))
        waypoint = int(request.POST.get('waypoint', None))
        atstep = int(request.POST.get('atstep', None))
        paths_query = "SELECT DISTINCT lc1.line_changes_id, h1.hexagram_id AS h1_id, h1.name AS h1_name, h2.hexagram_id AS h2_id, h2.name AS h2_name, h3.hexagram_id AS h3_id, h3.name AS h3_name, h4.hexagram_id AS h4_id, h4.name AS h4_name, h5.hexagram_id AS h5_id, h5.name AS h5_name, h6.hexagram_id AS h6_id, h6.name AS h6_name, h7.hexagram_id AS h7_id, h7.name AS h7_name FROM hexagram AS h1, hexagram AS h2, hexagram AS h3, hexagram AS h4, hexagram AS h5, hexagram AS h6, hexagram AS h7, line_changes AS lc1, line_changes AS lc2, line_changes AS lc3, line_changes AS lc4, line_changes AS lc5, line_changes AS lc6, line_changes AS lc7, line_changes AS lc8, line_changes AS lc9, line_changes AS lc10, line_changes AS lc11, line_changes AS lc12 WHERE lc1.chng_1 = 0 AND lc1.chng_2 = 0 AND lc1.chng_3 = 0 AND lc1.chng_4 = 0 AND lc1.chng_5 = 0 AND lc1.chng_6 = 0 AND lc1.hexagram = h1.hexagram_id AND lc1.line_1 = lc2.line_1 AND lc1.line_2 = lc2.line_2 AND lc1.line_3 = lc2.line_3 AND lc1.line_4 = lc2.line_4 AND lc1.line_5 = lc2.line_5 AND lc1.line_6 = lc2.line_6 AND lc2.chng_6 + lc2.chng_5 + lc2.chng_4 + lc2.chng_3 + lc2.chng_2 + lc2.chng_1 in (%s) AND lc2.hexagram = h2.hexagram_id AND lc3.chng_1 = 0 AND lc3.chng_2 = 0 AND lc3.chng_3 = 0 AND lc3.chng_4 = 0 AND lc3.chng_5 = 0 AND lc3.chng_6 = 0 AND lc3.hexagram = h2.hexagram_id AND lc3.line_1 = lc4.line_1 AND lc3.line_2 = lc4.line_2 AND lc3.line_3 = lc4.line_3 AND lc3.line_4 = lc4.line_4 AND lc3.line_5 = lc4.line_5 AND lc3.line_6 = lc4.line_6 AND lc4.chng_6 + lc4.chng_5 + lc4.chng_4 + lc4.chng_3 + lc4.chng_2 + lc4.chng_1 in (%s) AND lc4.hexagram = h3.hexagram_id AND lc5.chng_1 = 0 AND lc5.chng_2 = 0 AND lc5.chng_3 = 0 AND lc5.chng_4 = 0 AND lc5.chng_5 = 0 AND lc5.chng_6 = 0 AND lc5.hexagram = h3.hexagram_id AND lc5.line_1 = lc6.line_1 AND lc5.line_2 = lc6.line_2 AND lc5.line_3 = lc6.line_3 AND lc5.line_4 = lc6.line_4 AND lc5.line_5 = lc6.line_5 AND lc5.line_6 = lc6.line_6 AND lc6.chng_6 + lc6.chng_5 + lc6.chng_4 + lc6.chng_3 + lc6.chng_2 + lc6.chng_1 in (%s) AND lc6.hexagram = h4.hexagram_id AND lc7.chng_1 = 0 AND lc7.chng_2 = 0 AND lc7.chng_3 = 0 AND lc7.chng_4 = 0 AND lc7.chng_5 = 0 AND lc7.chng_6 = 0 AND lc7.hexagram = h4.hexagram_id AND lc7.line_1 = lc8.line_1 AND lc7.line_2 = lc8.line_2 AND lc7.line_3 = lc8.line_3 AND lc7.line_4 = lc8.line_4 AND lc7.line_5 = lc8.line_5 AND lc7.line_6 = lc8.line_6 AND lc8.chng_6 + lc8.chng_5 + lc8.chng_4 + lc8.chng_3 + lc8.chng_2 + lc8.chng_1 in (%s) AND lc8.hexagram = h5.hexagram_id AND lc9.chng_1 = 0 AND lc9.chng_2 = 0 AND lc9.chng_3 = 0 AND lc9.chng_4 = 0 AND lc9.chng_5 = 0 AND lc9.chng_6 = 0 AND lc9.hexagram = h5.hexagram_id AND lc9.line_1 = lc10.line_1 AND lc9.line_2 = lc10.line_2 AND lc9.line_3 = lc10.line_3 AND lc9.line_4 = lc10.line_4 AND lc9.line_5 = lc10.line_5 AND lc9.line_6 = lc10.line_6 AND lc10.chng_6 + lc10.chng_5 + lc10.chng_4 + lc10.chng_3 + lc10.chng_2 + lc10.chng_1 in (%s) AND lc10.hexagram = h6.hexagram_id AND lc11.chng_1 = 0 AND lc11.chng_2 = 0 AND lc11.chng_3 = 0 AND lc11.chng_4 = 0 AND lc11.chng_5 = 0 AND lc11.chng_6 = 0 AND lc11.hexagram = h6.hexagram_id AND lc11.line_1 = lc12.line_1 AND lc11.line_2 = lc12.line_2 AND lc11.line_3 = lc12.line_3 AND lc11.line_4 = lc12.line_4 AND lc11.line_5 = lc12.line_5 AND lc11.line_6 = lc12.line_6 AND lc12.chng_6 + lc12.chng_5 + lc12.chng_4 + lc12.chng_3 + lc12.chng_2 + lc12.chng_1 in (%s) AND lc12.hexagram = h7.hexagram_id AND h1.hexagram_id = %d AND %d in (h%d.hexagram_id) order by h1_id, h2_id, h3_id, h4_id, h5_id, h6_id, h7_id;" % (steps, steps, steps, steps, steps, steps, initial, waypoint, atstep+1)
        paths_result = LineChanges.objects.raw(paths_query)
        html=""
        length = 0
        if paths_result:
            for i, r in enumerate(paths_result):
                html += "<tr><td>%d</td><td>%d %s</td><td>%d %s</td><td>%d %s</td><td>%d %s</td><td>%d %s</td><td>%d %s</td><td>%d %s</td></tr>" % (i+1, r.h1_id, r.h1_name, r.h2_id, r.h2_name, r.h3_id, r.h3_name, r.h4_id, r.h4_name, r.h5_id, r.h5_name, r.h6_id, r.h6_name, r.h7_id, r.h7_name)
                length = i+1
        header="<!DOCTYPE html><html><head><style>table, th, td {border: 1px solid black; border-collapse: collapse; padding: 5px;}</style></head><body><h1>Inputs</h1><table><tr><th>Steps</th><th>Initial</th><th>Waypoint</th><th>atStep</th></tr><tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr></table><h1>%d Matches:</h1><table><tr><th>idx</th><th>Initial</th><th>Step 1</th><th>Step 2</th><th>Step 3</th><th>Step 4</th><th>Step 5</th><th>Step 6</th></tr>" % (steps, initial, waypoint, atstep, length)
        footer = "</table></body></html>"
        return HttpResponse(header + html + footer)
    else:
        return render(request, 'ichingdb/paths.html')

class ConsultationCreate(CreateView):
    model = Consultation
    fields = ['query', 'line_1', 'chng_1', 'line_2', 'chng_2', 'line_3', 'chng_3', 'line_4', 'chng_4', 'line_5', 'chng_5', 'line_6', 'chng_6']
    initial={'line_1':0,'line_2':0,'line_3':0,'line_4':0,'line_5':0,'line_6':0,'chng_1':0,'chng_2':0,'chng_3':0,'chng_4':0,'chng_5':0,'chng_6':0}

    def get_success_url(self):
        return reverse_lazy('ichingdb:reading', kwargs={'cid': self.object.consultation_id})

class ConsultationCreateRandom(CreateView):
    model = Consultation
    fields = ['query', 'line_1', 'chng_1', 'line_2', 'chng_2', 'line_3', 'chng_3', 'line_4', 'chng_4', 'line_5', 'chng_5', 'line_6', 'chng_6']

    def random_line(self, line_num):
        coin_1 = sample([2,3], k=1)[0]
        coin_2 = sample([2,3], k=1)[0]
        coin_3 = sample([2,3], k=1)[0]
        coin_sum = coin_1 + coin_2 + coin_3
        if coin_sum == 6:
            line = 0
            chng = 1
        elif coin_sum == 7:
            line = 1
            chng = 0
        elif coin_sum == 8:
            line = 0
            chng = 0
        else:
            line = 1
            chng = 1
#        print("line_num: %d, coin_sum: %d, line: %d, chng: %d" % (line_num, coin_sum, line, chng))
        return [line, chng]


    def get_initial(self):
        seed(datetime.now())
#        print(datetime.now())
        line_1, chng_1 = self.random_line(1)
        line_2, chng_2 = self.random_line(2)
        line_3, chng_3 = self.random_line(3)
        line_4, chng_4 = self.random_line(4)
        line_5, chng_5 = self.random_line(5)
        line_6, chng_6 = self.random_line(6)
        return {'line_1':line_1,'line_2':line_2,'line_3':line_3,'line_4':line_4,'line_5':line_5,'line_6':line_6,'chng_1':chng_1,'chng_2':chng_2,'chng_3':chng_3,'chng_4':chng_4,'chng_5':chng_5,'chng_6':chng_6}

    def get_success_url(self):
        return reverse_lazy('ichingdb:reading', kwargs={'cid': self.object.consultation_id})

class ConsultationUpdate(UpdateView):
    model = Consultation
    fields = ['notes','conclusion']

    def get_success_url(self):
        return reverse_lazy('ichingdb:reading', kwargs={'cid': self.object.consultation_id})

class ConsultationDelete(DeleteView):
    model = Consultation
    success_url = reverse_lazy('ichingdb:index')



