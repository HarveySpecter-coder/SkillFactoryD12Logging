from django.contrib import admin
from .models import Post, Subscribers, PostCategory, Author, Category
# Register your models here.


class CategoryFilter(admin.SimpleListFilter):
    title = 'Categories'
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        categories = set()
        for post in Post.objects.all():
            categories.update(post.categories.all())
        return [(category.id, category.new_category) for category in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(categories__in=[self.value()])

class PostCategoryInLine(admin.TabularInline):
    model = PostCategory
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = (PostCategoryInLine,)
    list_display = ('title', 'rating', 'author', 'display_categories')
    list_filter = ('author', CategoryFilter, 'rating')
    search_fields = ('title', 'rating', 'author__author__username', 'categories__new_category')

    def display_categories(self, obj):
        return ", ".join(category.new_category for category in obj.categories.all())

    display_categories.short_description = 'Categories'

class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_categories')
    list_filter = ('user',)
    search_fields = ('user__username', 'news_category__new_category')
    def display_categories(self, obj):
        return ", ".join(category.new_category for category in obj.news_category.all())

    display_categories.short_description = 'Categories'

admin.site.register(Post, PostAdmin)
admin.site.register(Subscribers, SubscribersAdmin)
admin.site.register(Author)
admin.site.register(Category)
