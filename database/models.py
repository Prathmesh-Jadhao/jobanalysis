from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    position = Column(String)
    company = Column(String)
    location = Column(String)
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    date = Column(String)
    description = Column(Text)

    skills = relationship("JobSkill", back_populates="job")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    skill_name = Column(String, unique=True, index=True, nullable=False)

    jobs = relationship("JobSkill", back_populates="skill")


class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)

    job = relationship("Job", back_populates="skills")
    skill = relationship("Skill", back_populates="jobs")
