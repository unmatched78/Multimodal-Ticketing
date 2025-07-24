from apps.qr.handler import QRMethod
from apps.nfc.handler import NFCMethod
from apps.nft.handler import NFTMethod
from apps.geofence.handler import GeoMethod
from apps.passbook.handler import PassbookMethod
from apps.biometric.handler import BiometricMethod

registry = {
    "qr": QRMethod(),
    "nfc": NFCMethod(),
    "nft": NFTMethod(),
    "geofence": GeoMethod(),
    "passbook": PassbookMethod(),
    "biometric": BiometricMethod()
}
