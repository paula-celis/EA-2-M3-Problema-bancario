"""Modelo de llegadas y servicio exponenciales para el problema bancario.

Uso: python simulacion.py [réplicas_por_escenario] [semilla]
La decisión de 70/30 se aplica a cada cliente. El intervalo exponencial se
toma de la fila del tipo elegido, según las medias de la guía.
"""
import csv, math, random, statistics, sys
from collections import defaultdict
from pathlib import Path

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 20261121
HORIZON = 480.0
DATA = {
 ('Retiro','Rápido'):(.23,1,1), ('Retiro','Normal'):(.40,2,2),
 ('Retiro','Lento'):(.17,3,3), ('Retiro','Muy lento'):(.20,3,4),
 ('Pago','Rápido'):(.10,1,3), ('Pago','Normal'):(.20,2,3),
 ('Pago','Lento'):(.30,3,5), ('Pago','Muy lento'):(.40,4,7),
}
SCENARIOS = {
 '3 cajas mixtas': ['Mixta','Mixta','Mixta'],
 '1 retiro + 2 pagos': ['Retiro','Pago','Pago'],
 '2 retiros + 1 pago': ['Retiro','Retiro','Pago'],
 '4 cajas (2 retiros + 2 pagos)': ['Retiro','Retiro','Pago','Pago'],
}

def draw_exp(mean, rng):
    return rng.expovariate(1.0 / mean)

def sample_customer(rng):
    action = 'Retiro' if rng.random() < .70 else 'Pago'
    choices = [(typ, *vals) for (act,typ), vals in DATA.items() if act == action]
    pick = rng.random(); cumulative = 0.0
    for typ, prob, mean_arrival, mean_service in choices:
        cumulative += prob
        if pick <= cumulative:
            return action, typ, mean_arrival, mean_service
    typ, prob, mean_arrival, mean_service = choices[-1]
    return action, typ, mean_arrival, mean_service

def run_rep(seed, teller_types):
    rng = random.Random(seed)
    available_at = [0.0] * len(teller_types)
    time = 0.0; observations=[]; counts=defaultdict(int)
    while True:
        action, typ, mean_arrival, mean_service = sample_customer(rng)
        time += draw_exp(mean_arrival, rng)
        if time >= HORIZON:
            break
        eligible = [i for i, kind in enumerate(teller_types)
                    if kind == 'Mixta' or kind == action]
        # La caja que primero queda libre recibe al usuario, con recorrido cero.
        idx = min(eligible, key=lambda i: available_at[i])
        start = max(time, available_at[idx])
        wait = start - time
        service = draw_exp(mean_service, rng)
        available_at[idx] = start + service
        observations.append((action, typ, idx + 1, wait, service))
        counts[(action,typ)] += 1
    waits=[x[3] for x in observations]
    teller_service=defaultdict(list)
    for action,typ,teller,wait,service in observations:
        teller_service[teller].append(service)
    teller_means={i:statistics.mean(v) for i,v in teller_service.items()}
    return counts, waits, teller_means, len(observations)

def main():
    out=Path(__file__).resolve().parents[1]/'outputs'; out.mkdir(exist_ok=True)
    result_rows=[]; teller_rows=[]
    for scenario_index,(scenario,teller_types) in enumerate(SCENARIOS.items()):
        for rep in range(1,N+1):
            counts, waits, teller_means, total = run_rep(SEED+scenario_index*100000+rep,teller_types)
            row={'escenario':scenario,'replica':rep,'total':total,
                 'espera_media_min':statistics.mean(waits) if waits else 0.0,
                 'espera_p95_min':sorted(waits)[math.ceil(.95*len(waits))-1] if waits else 0.0}
            for action in ('Retiro','Pago'):
                for typ in ('Rápido','Normal','Lento','Muy lento'):
                    row[f'{action}_{typ}']=counts[(action,typ)]
            result_rows.append(row)
            for teller,mean in teller_means.items():
                teller_rows.append([scenario,rep,teller,mean])
    with open(out/'resultados_replicas.csv','w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=result_rows[0].keys()); writer.writeheader(); writer.writerows(result_rows)
    with open(out/'tiempos_cajero.csv','w',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f); writer.writerow(['escenario','replica','cajero','tiempo_medio_servicio_min']); writer.writerows(teller_rows)
    print('réplicas por escenario:',N,'semilla:',SEED)
    for scenario in SCENARIOS:
        rs=[r for r in result_rows if r['escenario']==scenario]
        print(scenario,'usuarios/día prom=',round(statistics.mean(r['total'] for r in rs),1),
              'espera prom=',round(statistics.mean(float(r['espera_media_min']) for r in rs),2),
              'máx. espera media réplica=',round(max(float(r['espera_media_min']) for r in rs),2))
    print('Archivos escritos en',out)
if __name__=='__main__': main()
