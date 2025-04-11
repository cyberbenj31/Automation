
resource "cisco_loopback" "lo1" {
  name = "Loopback1"
  ip   = "1.1.1.1"
}

resource "cisco_loopback" "lo2" {
  name = "Loopback2"
  ip   = "2.2.2.2"
}

resource "cisco_loopback" "lo3" {
  name = "Loopback3"
  ip   = "3.3.3.3"
}