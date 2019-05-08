from rest_framework.routers import DefaultRouter

from adapost.views import IngrijitorViewSet, AnimalViewSet, RezervaViewSet, EvenimentViewSet

router = DefaultRouter()

router.register(r'ingrijitor', IngrijitorViewSet, base_name='ingrijitor')
router.register(r'animal', AnimalViewSet, base_name='animal')
router.register(r'rezerva', RezervaViewSet, base_name='rezerva')
router.register(r'eveniment', EvenimentViewSet, base_name='eveniment')

urlpatterns = router.urls
