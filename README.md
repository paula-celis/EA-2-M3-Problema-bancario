# Simulación de un problema bancario

Proyecto de simulación de colas bancarias para comparar cuatro configuraciones de cajas. El modelo utiliza llegadas y tiempos de servicio exponenciales, una jornada de 480 minutos y una proporción de 70 % de retiros y 30 % de pagos.

## Escenarios

- 3 cajas mixtas
- 1 caja de retiros + 2 cajas de pagos
- 2 cajas de retiros + 1 caja de pagos
- 2 cajas de retiros + 2 cajas de pagos

## Requisitos

Python 3. No se requieren paquetes externos.

## Ejecución

```bash
python simulacion.py 20 20261121
```

Los argumentos indican las réplicas por escenario y la semilla aleatoria. Si se omiten, se usan 20 réplicas y la semilla 20261121. El programa guarda `resultados_replicas.csv` y `tiempos_cajero.csv` en la carpeta `outputs`, junto a la carpeta del proyecto. Los CSV incluidos corresponden a 20 réplicas por escenario.

## Archivos

- `simulacion.py`: programa comentado de simulación.
- `resultados_replicas.csv`: resultados por escenario y réplica.
- `tiempos_cajero.csv`: tiempos de servicio por cajero.
- `EA3_Simulacion_Problema_Bancario_Paula_Celis_final.docx`: informe final corregido.
- `Informe_EA3_Simulacion_Bancaria.docx`: versión anterior del informe.

## Video de sustentación

[Ver el video en Google Drive](https://drive.google.com/file/d/1aTYnm91CIJcTaQdBrZe3CU_E8wrfRgX2/view)
