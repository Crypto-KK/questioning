from questioning.course.models import CourseName, CourseChapter, Course

import xadmin


class CourseNameAdmin:
    list_display = ['name', 'description', 'image']
    list_filter = ['name', 'description']
    search_fields = ['name', 'description']


class CourseChapterAdmin:
    list_display = ['title','parent_chapter']
    list_filter = ['title']
    search_fields = ['title']


class CourseAdmin:
    list_display = ['title', 'content','user', 'chapter', 'course_name']
    list_filter = ['content', 'title', 'created_at']
    search_fields = ['content', 'title']
    ordering = ['-created_at']
    readonly_fields = ['user']


xadmin.site.register(CourseName, CourseNameAdmin)
xadmin.site.register(CourseChapter, CourseChapterAdmin)
xadmin.site.register(Course, CourseAdmin)
