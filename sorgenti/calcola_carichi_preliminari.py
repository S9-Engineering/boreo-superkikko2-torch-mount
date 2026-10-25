"""Confronti statici di trave, non verifica della staffa su casco. Solo stdlib.

N, mm, MPa. 5g/10g sono scenari di sensibilita scelti, non requisiti di norma.
Non modifica il CAD; nessun dato di resistenza a caldo e disponibile.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
G=9.80665

def sezione(t,h,L,P,E,K):
    forte=t*h**3/12
    debole=h*t**3/12
    return {
        'spessore_mm':t,'altezza_mm':h,'lunghezza_mensola_mm':L,
        'forza_su_un_braccio_N':P,
        'sigma_forte_nominale_MPa':6*P*L/(t*h*h),
        'sigma_debole_nominale_MPa':6*P*L/(h*t*t),
        'sigma_forte_con_moltiplicatore_ipotetico_MPa':K*6*P*L/(t*h*h),
        'sigma_debole_con_moltiplicatore_ipotetico_MPa':K*6*P*L/(h*t*t),
        'freccia_forte_lineare_mm':P*L**3/(3*E*forte),
        'freccia_debole_lineare_mm':P*L**3/(3*E*debole),
    }

def main():
    scenari=[]
    for m in (.13,.2):
        for k in (1,5,10):
            F=m*G*k
            scenari.append({'massa_kg':m,'moltiplicatore_peso':k,'forza_totale_N':F,
                            'momento_a_50_mm_Nm':F*.05,'momento_a_70_mm_Nm':F*.07})
    confronti=[]
    for k in (1,5,10):
        P=.7*.2*G*k
        confronti.append({'scenario':{'massa_kg':.2,'moltiplicatore_peso':k,'quota_su_braccio':.7,
                         'E_assunto_MPa':1000,'moltiplicatore_tensione_assunto':2},
                         'sezione_esterna_ipotetica':sezione(6,18,70,P,1000,2)})
    out={
        'stato':'CALCOLO_PRELIMINARE_NON_VALIDAZIONE',
        'massa_corpo_dichiarata_kg':.13,
        'fonte_massa':'https://www.kikkolamp.com/superkikko2',
        'massa_progetto_assunta_kg':.2,
        'limite_massa':'Inclusione di cavo/viteria/staffa nei 130g e tolleranza non specificate; esemplare non pesato.',
        'modello':'Mensola retta prismatica, elastica lineare, piccole deformazioni; confronto per sezioni esterne, non simulazione CAD R03.',
        'formule':{'forza':'F=m*g*k','momento':'M=F*e','sigma':'M*c/I','freccia':'P*L^3/(3*E*I)'},
        'scenari_carico':scenari,'confronti_sezioni':confronti,
        'limiti':[
          '50/70mm di leva, 70% di ripartizione, 5g/10g, E1GPa e moltiplicatore2 sono ipotesi, non misure o prescrizioni.',
          'Il moltiplicatore2 non e un Kt misurato o limite superiore garantito.',
          'La R03 curva ha anche torsione, radici1.2mm, fori, contatti e serraggio non rappresentati dal comparatore.',
          'Nessuna curva di resistenza, modulo o creep in funzione di temperatura e tempo per la bobina reale.',
          'Una sezione6x18mm allesterno e soltanto un candidato: non risolve una radice libera1.2mm o il riscaldamento.',
          'Nessuna approvazione di materiale, supporto, configurazione casco o prova fisica.'
        ]}
    dest=ROOT/'verifiche/carichi-preliminari.json'
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(dest)

if __name__=='__main__':main()
