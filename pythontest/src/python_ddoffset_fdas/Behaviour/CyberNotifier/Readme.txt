Function Description£º
1¡¢The CyberNotifier shall notify the Integrated Surveillance System(ISS) <TCAS¢òInhibited> when TCAS¢ò alerts(as defined in LB1882) are inhibited in accordance with 
   FAA AC 20-151A Section 2-17.
2¡¢When <DMHDD[1/2/3/4/5]Available> are all valid and FALSE or invalid(or a combination thereof), the CyberNotifier shall assert <TCAS¢òInhibited>.
3¡¢The CyberNotifier shall only de-assert <TCAS¢òInhibited> when at least one of <DMHDD[1/2/3/4/5]Available> is Valid and Ture and there are no inhibited TCAS¢òalerts.
4¡¢When the highest priority "Active" and "Uninhibited" alert with an "auto pop" demand requires the Terrain Map Layer to be automatically presented to the crew, 
   the CyberNotifier shall set <MapFeatureRequest> to TERRAIN.
5¡¢When the highest priority "Active" and "Uninhibited" alert with an "auto pop" demand requires the Predictive Windshear Map Layer to be automatically presented 
   to the crew, the CyberNotifier shall set <MapFeatureRequest> to PREDICTIVE_WINDSHEAR.
6¡¢When no "Active" and "Uninhibited" alert have "auto pop" demands or when there are no "Active" and "Uninhibited" alerts, the CyberNotifier shall set <MapFeatureRequest>
   to NONE.
7¡¢The CyberNotifier shall only assert <CollapseAndHoldMenus> when there is an ¡°Active¡± and ¡°Uninhibited¡± Alert that requires the NAV and Main Menu to be collapsed 
   and Dropdowns to be disabled as defined by LB1882.
8¡¢The CyberNotifier shall set <CommandedSynopticPage> to the associated synoptic page of the highest absolute priority "Active" and "Uninhibited" Alert with 
   an associated page (where absolute priority and page association is defined by LB1882).
9¡¢The CyberNotifier shall assign <CommandedSynopticPage> to "None" when there are no Alerts "Active" and "Uninhibited" that affect a synoptic Page as defined by LB1882.
/****************************************************/
Add AlertBuffer Function.