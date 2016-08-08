Introduction:
  ditto is a service to associate packets/flows by building user activity trees and extracting features from activity trees.

Dependencies:
  Python 2.7.3 or 2.7.11 (tested on these two versions)
  Python Modules
    Pyshark 0.3.6.2 (tested on this version); threading; queue; time; glob; os; random; defaultdict; sys
  TShark 1.12.4 or 2.0.2 (tested on these two versions, but not sure whether other version still ​works fine)

Run:
  direct to ditto source folder
  live mode:
    python ditto.py -i "eth0" #ditto runs over interface "eth0"
  pcap mode:
    single pcap:
  python ditto.py -p "/srv/ditto/test.pcap" #ditto runs over "test.pcap" 
    folder containing pcap:
  python ditto.py -d "/srv/ditto/Dridex-set1" #ditto runs over all pcaps in "Dridex-set1"

Result:
  detailed:
    log.txt
  brief:
    run "python LogParser.py" first to take a look at brief output
    Each item in the result.txt is a feature value format
    output format: (grouped flow features)
    grouped flow features: [dst ip], [src port], [l2dn], [uri], [flowID], hit times
