from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blogs.models import Article
from blogs.services import get_articles_from_cache


class ArticleCreateView(CreateView):
    model = Article
    fields = ('name', 'description', 'image', 'created_at')
    success_url = reverse_lazy('blogs:list')


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        return get_articles_from_cache()


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.caunt_views += 1
        self.object.save()
        return self.object


class ArticleUpdatelView(UpdateView):
    model = Article
    fields = ('name', 'description', 'image', 'created_at')

    def get_success_url(self):
        return reverse('blogs:view', args=[self.kwargs.get('pk')])


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('blogs:list')
