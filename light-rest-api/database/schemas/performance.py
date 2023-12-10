from sqlalchemy import Column, Integer, String, Float
from app import ma, db


class Performance(db.Model):
    """ Table for computer performance data.
        Fields -> 'id', 'timestamp', 'memory_usage', 'cpu_usage', 'disk_usage'
    """
    __tablename__ = 'performance'
    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    memory_usage = Column(Float)
    cpu_usage = Column(Float)
    disk_usage = Column(Float)


class PerformanceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'timestamp', 'memory_usage', 'cpu_usage', 'disk_usage')


performance_schema = PerformanceSchema()
performances_schema = PerformanceSchema(many=True)
