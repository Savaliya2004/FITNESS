from rest_framework import serializers, viewsets, routers
from account.models import FitnessProfile
from store.models import MembershipPlan, Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessProfile
        fields = ['id', 'username', 'email', 'membership_type', 'fitness_goal', 'is_staff']

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class UserViewSet(viewsets.ModelViewSet):
    queryset = FitnessProfile.objects.all()
    serializer_class = UserSerializer

class MembershipViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'memberships', MembershipViewSet)
router.register(r'payments', PaymentViewSet)
