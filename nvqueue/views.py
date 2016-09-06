from django.db import transaction
from django.forms.models import model_to_dict

from nvqueue.models import Queue, Printjob
from nvqueue.serializers import QueueSerializer, PrintjobSerializer

from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.reverse import reverse


class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer

    @list_route(methods=['get'])
    def queue_by_name(self, request):
        """
        Returns queue object with the specified name or 404
        """
        queue_name = request.query_params.get('name')
        if not queue_name:
            return Response({'detail': 'valid queue name must be supplied'}, status=status.HTTP_404_NOT_FOUND)

        try:
            queue = Queue.objects.get(name=queue_name)
        except Queue.DoesNotExist:
            return Response({'detail': 'queue not found'}, status=status.HTTP_404_NOT_FOUND)

        # add instance URL
        queue_url = reverse('queue-detail', args=[queue.id], request=request)
        queue_dict = model_to_dict(queue)
        queue_dict['url'] = queue_url

        return Response(queue_dict, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def take_job(self, request, pk):
        """
        Normally called by printer services
        Returns the oldest job in this (FIFO) queue

        Inside a transaction it fetchs the next job, updates the printer field, and sets the state to 'printing'
        This prevents a race condition with concurrent access
        """
        queue = self.get_object()

        with transaction.atomic():
            oldest_job = queue.printjobs.filter(state='waiting').order_by('created').first()
            if not oldest_job:
                return Response({'detail': 'no more jobs'}, status=status.HTTP_404_NOT_FOUND)

            # add printer name and mark job as printing
            printer = request.data.get('printer')
            if not printer:
                return Response({'detail': 'printer must be supplied'}, status=status.HTTP_404_NOT_FOUND)

            oldest_job.printer = printer
            oldest_job.state='printing'
            oldest_job.save()

        return Response(model_to_dict(oldest_job), status=status.HTTP_202_ACCEPTED)


class PrintjobViewSet(viewsets.ModelViewSet):
    queryset = Printjob.objects.all()
    serializer_class = PrintjobSerializer

