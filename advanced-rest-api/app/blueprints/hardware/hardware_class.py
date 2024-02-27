from flask import request, jsonify, render_template
import psutil

from app.blueprints import BlueprintSingleton


class HardwareClass(BlueprintSingleton):
    """ Implements views related to hardware. """

    # private methods
    # views
    def performance(self):
        cpu = dict(
            usage=psutil.cpu_percent(),
            freq=psutil.cpu_freq()[0]
        )

        disk_stats = psutil.disk_usage('/')
        disk = dict(
            usage=disk_stats[3],
            total=disk_stats[0] / 10 ** 9,
            used=disk_stats[1] / 10 ** 9,
            free=disk_stats[2] / 10 ** 9
        )

        virtual_memory_stats = psutil.virtual_memory()
        virtual_memory = dict(
            usage=virtual_memory_stats[2],
            total=virtual_memory_stats[0] / 10 ** 9,
            available=virtual_memory_stats[1] / 10 ** 9,
            used=virtual_memory_stats[3] / 10 ** 9
        )
        return jsonify(
            cpu=cpu,
            disk=disk,
            virtual_memory=virtual_memory
        )

    # gui views
    def stats(self):
        return render_template('hardware/stats.html')
