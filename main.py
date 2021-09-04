#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Bot that tests the download and upload internet speed

"""
This Bot uses the speedtest-cli and iperf3 libraries to perform network measurements and tweepy to write tweets.

It runs a run for each library to get a measure of the total network throughput and the speed available from the hosts network perspective.
 
Usage:
Run this program using python main.py
"""

import logging
import speedtest
import os
import iperf3


def obtener_velocidad_internet_speedtest_cli():
    logging.info('Inicializando configuraciones speedtest-cli')
    try:
        test_velocidad_subida = speedtest.Speedtest()
    except:
        logging.error('Error al realizar la prueba con speedtest-cli velocidad subida')
        return -1, -1, ''
    try:
        test_velocidad_bajada = speedtest.Speedtest()
    except:
        logging.error('Error al realizar la prueba con speedtest-cli velocidad bajada')
        return -1, -1, ''
    logging.info('Iniciando prueba speedtest-cli de velocidad - Bajada')
    test_velocidad_bajada.download()
    logging.info('Iniciando prueba speedtest-cli  de velocidad - Subida')
    test_velocidad_subida.upload()
    logging.info('Pruebas de velocidad speedtest-cli  finalizadas')
    logging.info('Procesando resultados')
    velocidad_bajada = test_velocidad_bajada.results.download
    velocidad_subida = test_velocidad_subida.results.upload
    velocidad_bajada /= (1 * 10 **6)
    velocidad_subida /= (1 * 10 **6)
    logging.info('Resultados procesados')
    server = test_velocidad_bajada.results.server['sponsor']
    return velocidad_bajada,velocidad_subida,server

def obtener_velocidad_internet_iperf3():
    logging.info('Iniciando configuraciones iperf3')
    client = iperf3.Client()
    client.duration = 7
    client.server_hostname = 'iperf.scottlinux.com'
    client.port = 5201
    logging.info('Iniciando prueba iperf3')
    try:
        response = client.run()
    except:
        logging.error('Error al realizar la prueba con iperf3 ')
        return -1, -1
    logging.info('Prueba realizada exitosamente')
    logging.info('Procesando resultados')
    try:
        velocidad_bajada = response.received_Mbps
        velocidad_subida = response.sent_Mbps
    except:
        logging.error('Error al procesar resultados iperf3 ')
        return -1, -1
    logging.info('Resultados procesados')
    return velocidad_bajada, velocidad_subida


def main():
    HOST_NAME = str(os.environ['HOSTNAME'])
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO, filename='/log/{HOST_NAME}.log'.format(HOST_NAME=HOST_NAME))
    logging.info('Iniciando Pruebas de Velocidad....')
    vel_bajada,vel_subida,sponsor = obtener_velocidad_internet_speedtest_cli()
    if vel_bajada != -1 and vel_subida != -1:
        logging.info('speedtest-cli descarga - {descarga:3.2f} Mbits/s. Subida - {subida:3.2f} Mbits/s. Servidor - {servidor}'.format(descarga=vel_bajada, subida=vel_subida, servidor=sponsor))
        print('speedtest-cli descarga - {descarga:3.2f} Mbits/s. Subida - {subida:3.2f} Mbits/s. Servidor - {servidor}'.format(descarga=vel_bajada, subida=vel_subida, servidor=sponsor))
    else:
        logging.error('Error al realizar las pruebas, finalizando programa.')
        return -1
    vel_bajada,vel_subida = obtener_velocidad_internet_iperf3()
    if vel_bajada != -1 and vel_subida != -1:
        logging.info('iperf3 descarga - {descarga:.3f} Mbits/s. Subida - {subida:.3f} Mbits/s'.format(descarga=vel_bajada, subida=vel_subida))
        print('speedtest-cli descarga - {descarga:3.2f} Mbits/s. Subida - {subida:3.2f} Mbits/s. Servidor - {servidor}'.format(descarga=vel_bajada, subida=vel_subida, servidor='iperf3'))
    else:
        logging.error('Error al realizar las pruebas, finalizando programa.')
        return -1
    logging.info('Fin del programa')

if __name__ == '__main__':
    main()