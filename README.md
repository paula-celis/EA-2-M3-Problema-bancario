# Simulación de un problema bancario

Proyecto de simulación de colas de atención bancaria para comparar cuatro configuraciones de cajeros automáticos. El modelo usa llegadas y tiempos de servicio exponenciales, una jornada de 480 minutos y una proporción de 70 % de retiros y 30 % de pagos.

## Escenarios

- 3 cajas mixtas
- 1 caja de retiros + 2 cajas de pagos
- 2 cajas de retiros + 1 caja de pagos
- 2 cajas de retiros + 2 cajas de pagos

## Requisitos

Python 3. No requiere instalar paquetes externos.

## Ejecución

```bash
python simulacion.py 20 20261121
```

Los argumentos indican la cantidad de réplicas por escenario y la semilla aleatoria. Si se omiten, el programa usa 20 réplicas y la semilla 20261121.

El programa guarda `resultados_replicas.csv` y `tiempos_cajero.csv` en la carpeta `outputs`, ubicada junto a la carpeta del proyecto. Los CSV incluidos en este repositorio corresponden a 20 réplicas por escenario.

## Archivos

- `simulacion.py`: programa de simulación.
- `resultados_replicas.csv`: resultados por escenario y réplica.
- `tiempos_cajero.csv`: tiempos de servicio por cajero.
- `Informe_EA3_Simulacion_Bancaria.docx`: informe del trabajo.
