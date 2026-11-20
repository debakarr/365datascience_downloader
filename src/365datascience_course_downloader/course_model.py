
from __future__ import annotations

from typing import List, Optional, Union, Dict, Any

from pydantic import BaseModel, Field, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class Info(Model):
    name: str
    slug: Optional[str] = None
    free: bool
    paid_access: bool = Field(..., alias="paidAccess")
    reviewed: Optional[bool] = None
    small_image: Optional[str] = Field(None, alias="smallImage")


class Stats(Model):
    text_lessons: Optional[int] = Field(None, alias="textLessons")
    text_lessons_duration: Optional[float] = Field(None, alias="textLessonsDuration")
    video_lessons: Optional[int] = Field(None, alias="videoLessons")
    video_lessons_duration: Optional[float] = Field(None, alias="videoLessonsDuration")
    exercises: Optional[int] = None
    coding_exercises: Optional[int] = Field(None, alias="codingExercises")
    downloadable_resources: Optional[int] = Field(None, alias="downloadableResources")
    practice_exams: Optional[int] = Field(None, alias="practiceExams")
    practice_exams_duration: Optional[float] = Field(None, alias="practiceExamsDuration")
    projects: Optional[int] = None
    projects_duration: Optional[float] = Field(None, alias="projectsDuration")
    course_projects: Optional[int] = Field(None, alias="courseProjects")
    course_exams: Optional[int] = Field(None, alias="courseExams")
    lecture_downloadables: int = Field(..., alias="lectureDownloadables")
    lecture_downloadables_free: int = Field(..., alias="lectureDownloadablesFree")
    lectures: int


class NextLecture(Model):
    section_id: int = Field(..., alias="sectionId")
    id: int
    slug: str
    name: str


class Progress(Model):
    total: int
    completed: int


class VideoItem(Model):
    name: Optional[str] = None
    ext_id: str = Field(..., alias="extId")
    provider: str
    duration: int
    duration_seconds: float = Field(..., alias="durationSeconds")
    id: int


class Downloadable(Model):
    id: Optional[int] = None
    name: str
    file: str
    extension: Optional[str] = None
    downloadable_assignment: Optional[int] = Field(
        None, alias="downloadableAssignment"
    )


class Notes(Model):
    list: List[Dict[str, Any]] = Field(default_factory=list)
    count: int = 0


class Next(Model):
    asset: Union[bool, Asset]


class Asset(Model):
    type: str
    order: Optional[str] = None
    id: int
    slug: Optional[str] = None
    name: str

    review: Optional[bool] = None
    free: Optional[Union[bool, int]] = None
    duration: Optional[int] = None
    completed: Optional[Union[bool, int]] = None
    unlocked: Optional[bool] = None
    useful_or_not: Optional[bool] = Field(None, alias="usefulOrNot")

    video: Optional[Union[bool, VideoItem]] = None
    assignment: Optional[bool] = None
    quiz: Optional[bool] = None
    practice_exam: Optional[bool] = Field(None, alias="practiceExam")

    downloadables: Optional[List[Downloadable]] = None
    next: Optional[Next] = None

    questions: Optional[int] = None
    questions_count: Optional[int] = Field(None, alias="questionsCount")
    lecture_id: Optional[int] = Field(None, alias="lectureId")
    section_id: Optional[int] = Field(None, alias="sectionId")

    text: Optional[str] = None
    cases: Optional[int] = None

    has_code_along: Optional[bool] = Field(None, alias="hasCodeAlong")
    has_transcript: Optional[int] = Field(None, alias="hasTranscript")
    notes: Optional[Notes] = None

    last_user_exam_id: Optional[int] = Field(None, alias="lastUserExamId")
    button: Optional[Dict[str, Any]] = None


class Section(Model):
    order: int
    id: Optional[int] = None
    name: str
    image: Optional[str] = None
    free: Optional[bool] = None
    duration: int
    completed: Optional[bool] = None
    progress: Progress
    assets: List[Asset]
    type: Optional[str] = None


class GettingStartedStep(Model):
    earn_way_name: str = Field(..., alias="earnWayName")
    earn_way_key: str = Field(..., alias="earnWayKey")
    earn_way_xp: int = Field(..., alias="earnWayXp")
    earn_way_coins: Optional[int] = Field(None, alias="earnWayCoins")
    is_completed: Optional[Union[bool, int]] = Field(None, alias="isCompleted")


class GettingStarted(Model):
    steps: List[GettingStartedStep]
    certificate: Dict[str, Any] = Field(default_factory=dict)


class CourseModel(Model):
    id: int
    slug: str
    updated: Optional[str] = None
    info: Info
    exam_id: int = Field(..., alias="examId")
    stats: Stats
    next_lecture: NextLecture = Field(..., alias="nextLecture")
    sections: List[Section]
    getting_started: Optional[GettingStarted] = Field(
        None, alias="gettingStarted"
    )


Next.model_rebuild()
