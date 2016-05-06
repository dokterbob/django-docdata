from os import path

from httmock import HTTMock

from docdata.models import PaymentCluster
from docdata.exceptions import PaymentStatusException

from .base import PaymentTestBase


class OfflinePaymentTests(PaymentTestBase):
    """ Tests not requiring payment credentials to be set. """

    def test_status_fail(self):
        """ Test whether status_change requests are handled well."""

        url = self.status_change_url

        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 404)

        response = self.client.get(url+'?merchant_transaction_id=kaas')
        self.failUnlessEqual(response.status_code, 404)

    def test_transaction_id(self):
        """ Test transaction_id -> pk resolution. """

        pc = PaymentCluster(pk=self.get_transaction_id())
        pc.save()

        transaction_id = pc.transaction_id
        pc2 = PaymentCluster.get_by_transaction_id(transaction_id)

        self.assertEqual(pc.pk, pc2.pk)

    def read_file(self, filename):
        """ Read contents from file in current directory. """

        filename = path.join(path.dirname(__file__), filename)

        return open(filename).read()

    def test_status_xml_std(self):
        """ Test parsing the xml_std status report. """

        # Setup a mock
        def report_xml_std_mock(url, request):
            return self.read_file('report_xml_std.xml')

        with HTTMock(report_xml_std_mock):
            result = self.interface.status_payment_cluster(
                report_type='xml_std',
                merchant_name='yolo',
                merchant_password='yolo2',
                payment_cluster_key=(

                )
            )

            self.assertEquals(result, {
                'meta_considered_safe': 'false',
                'meta_charged_back': 'N',
                'meta_amount_received': 'none',
                'payment_cluster_process': 'started',
                'last_partial_payment_process': 'new',
                'payout_process': 'new',
                'last_partial_payment_method': 'acceptgironew-nl-nlg'
            })

    def test_status_txt_simple(self):
        """ Test parsing the txt_simple status report. """

        # Success
        with HTTMock(lambda url, request: 'Y'):
            result = self.interface.status_payment_cluster(
                report_type='txt_simple',
                merchant_name='yolo',
                merchant_password='yolo2',
                payment_cluster_key=self.default_payment_cluster_key
            )

            self.assertEquals(result, True)

        # Fail
        with HTTMock(lambda url, request: 'N'):
            result = self.interface.status_payment_cluster(
                report_type='txt_simple',
                merchant_name='yolo',
                merchant_password='yolo2',
                payment_cluster_key=self.default_payment_cluster_key
            )

            self.assertEquals(result, False)

        # Weird status
        with HTTMock(lambda url, request: 'bananas'):
            self.assertRaises(
                PaymentStatusException,
                lambda: self.interface.status_payment_cluster(
                    report_type='txt_simple',
                    merchant_name='yolo',
                    merchant_password='yolo2',
                    payment_cluster_key=self.default_payment_cluster_key
                )
            )

    def test_status_txt_simple2(self):
        """ Test parsing the txt_simple2 status report. """

        # Success
        with HTTMock(lambda url, request: 'YY'):
            result = self.interface.status_payment_cluster(
                report_type='txt_simple2',
                merchant_name='yolo',
                merchant_password='yolo2',
                payment_cluster_key=self.default_payment_cluster_key
            )

            self.assertEquals(result['paid'], True)
            self.assertEquals(result['closed'], True)

        # Fail
        with HTTMock(lambda url, request: 'NN'):
            result = self.interface.status_payment_cluster(
                report_type='txt_simple2',
                merchant_name='yolo',
                merchant_password='yolo2',
                payment_cluster_key=self.default_payment_cluster_key
            )

            self.assertEquals(result['paid'], False)
            self.assertEquals(result['closed'], False)

        # Weird status
        with HTTMock(lambda url, request: 'bananas'):
            self.assertRaises(
                PaymentStatusException,
                lambda: self.interface.status_payment_cluster(
                    report_type='txt_simple2',
                    merchant_name='yolo',
                    merchant_password='yolo2',
                    payment_cluster_key=self.default_payment_cluster_key
                )
            )
