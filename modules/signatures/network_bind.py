# Copyright (C) 2013 Claudio "nex" Guarnieri (@botherder)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lib.cuckoo.common.abstracts import Signature

class NetworkBIND(Signature):
    name = "network_bind"
    description = "Starts a server listening on {0}:{1}"
    severity = 2
    categories = ["bind"]
    authors = ["nex"]
    minimum = "0.5"

    def run(self):
        for process in self.results["behavior"]["processes"]:
            for call in process["calls"]:
                if call["api"] != "bind":
                    continue

                ip = None
                port = None

                for argument in call["arguments"]:
                    if argument["name"] == "ip":
                        ip = argument["value"]
                    elif argument["name"] == "port":
                        port = argument["value"]
                
                if ip and port:
                    self.description = self.description.format(ip, port)
                    return True

        return False
