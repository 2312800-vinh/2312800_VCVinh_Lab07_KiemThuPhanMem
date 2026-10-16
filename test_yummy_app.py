import unittest
from unittest.mock import patch

from yummy_app import YummyApp
import gps_service


# ================================================================
# CAP DO 1: Bo test co ban cho san (Moi chi dat ~35% Coverage)
# ================================================================
class TestEasyLevel(unittest.TestCase):
    """Kiem thu chuc nang co ban tinh tien don hang"""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)


# ================================================================
# CAP DO 2 (TIET 3): Test case tu viet - 4 kich ban apply_promo_code
# Bang thiet ke viet tay: xem BaoCao_KetQua_Lab7.docx (muc 2)
# ================================================================
class TestMediumLevel(unittest.TestCase):
    """Kiem thu ma khuyen mai: online, offline, rang buoc phien ban HDH."""

    def test_online_valid_promo_applies_discount(self):
        app = YummyApp(network_status="online", os_version=15)
        self.assertAlmostEqual(app.apply_promo_code(100000, "GIAM10"), 90000)

    def test_offline_raises_connection_error(self):
        app = YummyApp(network_status="offline", os_version=15)
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_special_promo_on_os15_applies_discount(self):
        app = YummyApp(network_status="online", os_version=15)
        self.assertAlmostEqual(app.apply_promo_code(100000, "NEW_OS_ONLY"), 80000)

    def test_special_promo_on_os14_raises_value_error(self):
        app = YummyApp(network_status="online", os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")


# ================================================================
# CAP DO 2 (TIET 3): Test case tu viet - 3 kich ban get_nearby_restaurants
# Dung @patch de gia lap GPS (dong the phan cung)
# ================================================================
class TestHardLevel(unittest.TestCase):
    """Kiem thu de xuat nha hang lan can voi GPS gia lap."""

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_inside_region_returns_restaurants(self, mock_location):
        mock_location.return_value = (10.0, 105.0)
        app = YummyApp()
        self.assertEqual(
            app.get_nearby_restaurants(),
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
        )

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_outside_region_returns_empty_list(self, mock_location):
        mock_location.return_value = (20.0, 110.0)
        app = YummyApp()
        self.assertEqual(app.get_nearby_restaurants(), [])

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_signal_lost_returns_error_message(self, mock_location):
        mock_location.side_effect = gps_service.GPSSignalLostError()
        app = YummyApp()
        self.assertEqual(
            app.get_nearby_restaurants(),
            "Khong the xac dinh vi tri.",
        )


if __name__ == "__main__":
    unittest.main()
