from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from random import seed, sample
from ichingdb.models import Consultation
from datetime import datetime

def index(request):
#    seed(datetime.now())
    consultation_list = reversed(Consultation.objects.all())
    return render(request, 'ichingdb/index.html', {'consultation_list': consultation_list})

def reading(request, cid):
#    seed(datetime.now())
    simple_query = "SELECT DISTINCT consultation_id, query, lc.hexagram AS initial, CASE WHEN MOD(lc.hexagram, 2) = 1 THEN 'inspiration' ELSE 'manifestation' END AS initial_type, h.name AS initial_name, h.description AS initial_desc, pair.hexagram2 AS mirror, CASE WHEN MOD(pair.hexagram2, 2) = 1 THEN 'inspiration' ELSE 'manifestation' END AS mirror_type, h2.name AS mirror_name, h2.description AS mirror_desc, notes, conclusion FROM consultation JOIN line_changes AS lc USING (line_1 , line_2 , line_3 , line_4 , line_5 , line_6) JOIN hexagram AS h ON h.hexagram_id = lc.hexagram, hexagram AS h2, pair WHERE lc.chng_1 = 0 AND lc.chng_2 = 0 AND lc.chng_3 = 0 AND lc.chng_4 = 0 AND lc.chng_5 = 0 AND lc.chng_6 = 0 AND pair.hexagram1_id = lc.hexagram AND h2.hexagram_id = pair.hexagram2 AND consultation_id = %d;" % cid
    line_query = "SELECT C.consultation_id, lc2.hexagram AS result, h1.name AS result_name, h1.description result_desc, hl.h_line_position AS line, hlp.name AS line_name, hlp.meaning AS line_desc, hl.related_hexagram AS context, h3.name AS context_name, h3.description AS context_desc, hl.translation AS line_trans, hl.commentary AS line_comm, hl2.h_line_position AS m_line, hlp2.name AS m_line_name, hlp2.meaning AS m_line_desc, hl2.related_hexagram AS m_context, h4.name AS m_context_name, h4.description AS m_context_desc, hl2.translation AS m_trans, hl2.commentary AS m_comm FROM consultation AS C JOIN line_changes AS lc USING (line_1 , line_2 , line_3 , line_4 , line_5 , line_6) JOIN line_changes AS lc2 USING (line_1 , line_2 , line_3 , line_4 , line_5 , line_6) JOIN hexagram AS h ON h.hexagram_id = lc.hexagram JOIN hexagram AS h1 ON h1.hexagram_id = lc2.hexagram, hexagram AS h2, pair, hexagram_line AS hl, hexagram AS h3, hexagram_line AS hl2, hexagram AS h4, h_line_position AS hlp, h_line_position AS hlp2 WHERE lc.chng_1 = 0 AND lc.chng_2 = 0 AND lc.chng_3 = 0 AND lc.chng_4 = 0 AND lc.chng_5 = 0 AND lc.chng_6 = 0 AND lc2.chng_1 = C.chng_1 AND lc2.chng_2 = C.chng_2 AND lc2.chng_3 = C.chng_3 AND lc2.chng_4 = C.chng_4 AND lc2.chng_5 = C.chng_5 AND lc2.chng_6 = C.chng_6 AND hl.hexagram = lc.hexagram AND hl.related_hexagram = h3.hexagram_id AND ((hl.h_line_position = 1 AND lc2.chng_1 = 1) OR (hl.h_line_position = 2 AND lc2.chng_2 = 1) OR (hl.h_line_position = 3 AND lc2.chng_3 = 1) OR (hl.h_line_position = 4 AND lc2.chng_4 = 1) OR (hl.h_line_position = 5 AND lc2.chng_5 = 1) OR (hl.h_line_position = 6 AND lc2.chng_6 = 1)) AND pair.hexagram1_id = lc.hexagram AND hl2.hexagram = pair.hexagram2 AND hl2.h_line_position = 7 - hl.h_line_position AND h4.hexagram_id = hl2.related_hexagram AND h2.hexagram_id = pair.hexagram2 AND hl.h_line_position = hlp.h_line_position_id AND hl2.h_line_position = hlp2.h_line_position_id AND consultation_id = %d;" % cid
    c = get_object_or_404(Consultation, pk=cid)
    simple_result = Consultation.objects.raw(simple_query)
    if c.chng_1 == 1 or c.chng_2 == 1 or c.chng_3 == 1 or c.chng_4 == 1 or c.chng_5 == 1 or c.chng_6 == 1:
        line_result = Consultation.objects.raw(line_query)
        return render(request, 'ichingdb/reading.html', {'cid': cid, 'simple_result': simple_result,'line_result': line_result})
    return render(request, 'ichingdb/reading.html', {'cid': cid, 'simple_result': simple_result,'line_result': False})


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



