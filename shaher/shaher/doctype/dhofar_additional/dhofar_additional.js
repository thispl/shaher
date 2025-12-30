// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("DHOFAR ADDITIONAL", {
	refresh(frm) {
        if (!frm.doc.__islocal && frm.doc.docstaus != 2){
            frm.add_custom_button(__('Create Additional Work'), function () {
            newdoc = frappe.model.make_new_doc_and_get_name('ADDITIONAL WORK');
            newdoc = locals['ADDITIONAL WORK'][newdoc];
            newdoc.against = 'DHOFAR ADDITIONAL'; 
            newdoc.additional_work_against = 'DHOFAR';
            newdoc.reference_id = frm.doc.name;
            newdoc.month=frm.doc.month;
            newdoc.year=frm.doc.year;
            newdoc.invoice_from=frm.doc.invoice_from;
            newdoc.invoice_upto=frm.doc.invoice_upto;
            frappe.set_route("Form", "ADDITIONAL WORK", newdoc.name);
            });
        }
        frm.fields_dict["base_manpower"].grid.cannot_add_rows = true;
        frm.fields_dict["base_manpower"].grid.wrapper.find('.grid-remove-rows').hide();
        frm.fields_dict["base_manpower"].grid.only_sortable = false;
        frm.fields_dict["base_manpower"].refresh();
        frm.fields_dict["base_vehicle"].grid.cannot_add_rows = true;
        frm.fields_dict["base_vehicle"].grid.wrapper.find('.grid-remove-rows').hide();
        frm.fields_dict["base_vehicle"].grid.only_sortable = false;
        frm.fields_dict["base_vehicle"].refresh();
        frm.fields_dict["base_vehicle_cost_per_trip"].grid.cannot_add_rows = true;
        frm.fields_dict["base_vehicle_cost_per_trip"].grid.wrapper.find('.grid-remove-rows').hide();
        frm.fields_dict["base_vehicle_cost_per_trip"].grid.only_sortable = false;
        frm.fields_dict["base_vehicle_cost_per_trip"].refresh();
        frm.fields_dict["airconditioning_system_spare_parts"].grid.cannot_add_rows = true;
        frm.fields_dict["airconditioning_system_spare_parts"].grid.wrapper.find('.grid-remove-rows').hide();
        frm.fields_dict["airconditioning_system_spare_parts"].grid.only_sortable = false;
        frm.fields_dict["airconditioning_system_spare_parts"].refresh();
        frm.fields_dict["ff_systems_spare_parts"].grid.cannot_add_rows = true;
        frm.fields_dict["ff_systems_spare_parts"].grid.wrapper.find('.grid-remove-rows').hide();
        frm.fields_dict["ff_systems_spare_parts"].grid.only_sortable = false;
        frm.fields_dict["ff_systems_spare_parts"].refresh();
        
        if (frm.doc.__islocal){
            const currentYear = new Date().getFullYear();
            frm.set_value('year', currentYear);
            const manpowerData = [
                ["Electrical Engineer", 225.000],
                ["Civil Engineer", 180.000],
                ["Cable Jointer 33KV", 225.000],
                ["Asst. Cable Jointer 33KV", 165.000],
                ["Cable Jointer 132, 220 & 400 KV", 1650.000],
                ["Asst. Cable Jointer 132, 220 & 400 KV", 1050.000],
                ["MEP Technician (Fire Fighting System)", 150.000],
                ["MEP Supervisor", 180.000],
                ["Civil Supervisor", 150.000],
                ["Document Controller", 105.000],
                ["Mechanical Technician", 165.000],
                ["Painter", 135.000],
                ["Fire Alarm System Technician (Electronic Background)", 165.000]
                ];

            frm.clear_table("base_manpower");
            manpowerData.forEach(([description, unit_price]) => {
                let row = frm.add_child("base_manpower");
                row.description = `(${description})`;
                row.unit_price = unit_price;
            });
            let row = frm.add_child("base_manpower");
            row.description = `Total`;
            row.unit_price = 0;
            frm.refresh_field("base_manpower");
            const vehicleData = [
    ["(Hiab) 3 TON", 1900, 0, 0],
    ["(Hiab) 5 TON", 2000, 0, 0],
    ["(Hiab) 10 TON & Above", 1200, 0, 0],
    ["Emergency vehicle", 650, 0, 0],
    ["Crane 25 TON", 3000, 0, 0],
    ["Crane 50 TON", 4000, 0, 0],
    ["Crane 100 TON & Above", 3000, 0, 0],
    ["Washing Skid", 750, 0, 0],
    ["Canter 5 Ton", 600, 0, 0],
    ["Low Bed trailer", 2500, 0, 0],
    ["Flat Bed trailer", 2500, 0, 0],
    ["JCB", 900, 0, 0],
    ["Shovel", 4500, 0, 0],
    ["Grader", 4500, 0, 0],
    ["Excavator", 4500, 0, 0],
    ["Bucket truck", 4800, 0, 0],
    ["Cable Puller Machine", 900, 0, 0],
    ["Conductor stringing machine suitable for 132kV, 220kV & 400kV", 3000, 0, 0],
    ["Winch Machine 10 Ton", 2000, 0, 0],
    ["Portable Diesel Generator (350 KVA)", 650, 0, 0],
    ["Sag Bridge up to 400kV.", 450, 1, 450],
    ["Man lifter machine", 900, 0, 0],
    ["Cable Jack", 300, 0, 0],
    ["Welding set Potable", 500, 0, 0],
    ["Hydraulic crimping tool suitable for 132kV, 220kV & 400 kV", 1250, 0, 0],
    ["OHL Trolly (cycle) suitable for 132kV, 220kV & 400 kV", 225, 1, 225],
    ["Come Along Clamps suitable for 132kV, 220kV & 400 kV.", 35, 4, 140],
    ["Lever chain hoist suitable for 132kV, 220kV & 400 kV.", 50, 6, 300],
    ["Snatch block 1 Ton", 10, 0, 0],
    ["Snatch block 2 Ton", 12, 2, 24],
    ["Snatch block 3 Ton", 15, 1, 15],
    ["Snatch block 6 Ton", 30, 0, 0],
    ["Working Platform for OPGW - 7mtr", 75, 6, 450],
    ["Hook Ladder - 6mtr", 35, 6, 210],
    ["Hydraulic Conductor Cutter (Steel Dragon)", 25, 6, 150],
    ["Wire Rope Steel Sling 200mtr x 14mm", 25, 6, 150],
    ["Bow Shackle 4.75 ton", 5, 24, 120],
    ["Bow Shackle 6.5 ton", 6, 24, 144],
    ["Bow Shackle 8.5 ton", 8, 12, 96],
    ["Wire Rope Steel Sling 2mtr x 12mm", 2, 24, 48],
    ["Wire Rope Steel Sling 1mtr x 18mm", 2, 12, 24],
    ["PP Rope 200mtr x 12mm", 8, 6, 48],
    ["PP Rope 200mtr x 18mm", 10, 6, 60],
    ["PP Rope 200mtr x 20mm", 12, 6, 72],
    ["Snatch block 5 Ton", 25, 12, 300],
    ["Snatch block 4 Ton", 20, 2, 40],["Total",0,0,0]
];





            frm.clear_table("base_vehicle");
            vehicleData.forEach(([description, unit_price, qty,amnt]) => {
                let row = frm.add_child("base_vehicle");
                row.description = description;
                row.unit_price = unit_price;
                row.total_provided=qty;
                row.total_claim_this_month=amnt;
                row.amount_to_be_paid=amnt;
            });
            frm.refresh_field("base_vehicle");
            const vehiclepertrip = [
                ["Water tanker 650 Gallon for GS", 20.000],
                ["Water tanker 1300 Gallon for GS", 40.000],
                ["Water tanker 5000 Gallon for GS", 90.000],
                ["Water tanker 10000 Gallon for GS", 200.000],
                ["Drainage tanker 5000 Gallon for GS", 90.000],["Total",0]
            ];

            frm.clear_table("base_vehicle_cost_per_trip");
            vehiclepertrip.forEach(([ description,unit_price]) => {
                let row = frm.add_child("base_vehicle_cost_per_trip");
                row.unit_price = unit_price;
                row.description = description;
            });
            frm.refresh_field("base_vehicle_cost_per_trip");
            const acPartsData = [
                ["Compressor for 5 TON capacity (Standalone AC)", "1 No.", 750.000],
                ["Compressor for 10 TON capacity", "1 No.", 1250.000],
                ["Compressor for 15 TON capacity", "1 No.", 2500.000],
                ["Compressor for 20 TON capacity", "1 No.", 3250.000],
                ["Compressor for 25 TON capacity", "1 No.", 5250.000],
                ["Compressor for 30 TON capacity", "1 No.", 7250.000],
                ["Compressor for 35 TON capacity", "1 No.", 8250.000],
                ["Compressor for 40 TON capacity", "1 No.", 9850.000],
                ["Compressor for 45 TON capacity", "1 No.", 10950.000],
                ["Compressor for 50 TON capacity", "1 No.", 13450.000],
                ["Compressor for 55 TON capacity", "1 No.", 15650.000],
                ["Compressor for 60 TON capacity", "1 No.", 17950.000],
                ["Compressor contactors", "1 No.", 125.000],
                ["Condenser fan blade", "1 No.", 230.000],
                ["Condenser fan motor", "1 No.", 750.000],
                ["Expansion valve", "1 No.", 190.000],
                ["HP ILP Switch", "1 No.", 45.000],
                ["Indoor fan casing", "1 No.", 275.000],
                ["Indoor fan runner", "1 No.", 360.000],
                ["Timer relays", "1 No.", 65.000],
                ["Auxiliary relay", "1 No.", 55.000],
                ["Blower shaft", "1 No.", 425.000],
                ["Blower wheel", "1 No.", 575.000],
                ["Changeover switch", "1 No.", 95.000],
                ["Crank case heater", "1 No.", 275.000],
                ["Electrical logic panel", "1 No.", 560.000],
                ["Over current relay for compressor", "1 No.", 125.000],
                ["Overcurrent relay for condenser fan motor", "1 No.", 85.000],
                ["Pilot relay", "1 No.", 88.000],
                ["Blower shaft pulley", "1 No.", 195.000],
                ["Indoor fan motor pulley", "1 No.", 190.000],
                ["Fan motor rain guard", "1 No.", 225.000],
                ["Prefilter (Aluminum)", "1 No.", 195.000],
                ["Solenoid valve", "1 No.", 215.000],
                ["Terminal base", "1 No.", 35.000],
                ["Thermistor", "1 No.", 45.000],
                ["Thermostat (Electronic)", "1 No.", 55.000],
                ["Thermostat (Manual)", "1 No.", 48.000],
                ["Shaft modification for bearing replacement", "1 No.", 285.000],
                ["Repair and programming of control module", "1 No.", 415.000],
                ["Micro-process control board", "1 No.", 675.000],
                ["Re-winding & overhauling of semi sealed compressor without spares", "1 No.", 310.000],
                ["Transformer for AC", "1 No.", 125.000],
                ["Blower bush", "1 No.", 168.000],
                ["Dual pressure switch", "1 No.", 195.000],
                ["Dual pole switch", "1 No.", 188.000],
                ["Surge absorber", "1 No.", 245.000],
                ["Blower bearing", "1 No.", 325.000],
                ["Panel board control module", "1 No.", 415.000],
                ["Mechanical timer", "1 No.", 125.000],
                ["Contractor FM & IBM", "1 No.", 186.000],
                ["Swing motor", "1 No.", 350.000],
                ["Fan Cycling switch", "1 No.", 145.000],
                ["Oil pressure switch", "1 No.", 185.000],
                ["Filter drier", "1 No.", 280.000],
                ["Hose", "1 No.", 188.000],
                ["Cooling coil", "1 No.", 306.000],
                ["Indoor temperature sensor", "1 No.", 56.000],
                ["Ambient temperature sensor", "1 No.", 190.000],["Total","",0]
                ];
            frm.clear_table("airconditioning_system_spare_parts");
            acPartsData.forEach(([ description,uom,unit_price]) => {
                let row = frm.add_child("airconditioning_system_spare_parts");
                row.unit_price = unit_price;
                row.description = description;
                row.uom = uom;
            });
            frm.refresh_field("airconditioning_system_spare_parts");

            const ffPartsData = [
                ["Seamless GI Pipe Dia 1/2\"", "1 mtr", 1.600],
                ["Seamless GI Pipe Dia 1\"", "1 mtr", 3.200],
                ["Seamless GI Pipe Dia 1.1/2\"", "1 mtr", 4.400],
                ["Seamless GI Pipe Dia 2\"", "1 mtr", 4.800],
                ["Seamless GI Pipe Dia 2.1/2\"", "1 mtr", 5.600],
                ["Seamless GI Pipe Dia 3\"", "1 mtr", 8.400],
                ["Seamless GI Pipe Dia 4\"", "1 mtr", 12.000],
                ["Seamless GI Pipe Dia 5\"", "1 mtr", 14.400],
                ["Seamless GI Pipe Dia 6\"", "1 mtr", 20.000],
                ["B. S Pipe Dia 1/2\"", "1 mtr", 3.200],
                ["B. S. Pipe Dia 1\"", "1 mtr", 4.800],
                ["B.S. Pipe Dia 1.1/2\"", "1 mtr", 6.400],
                ["B.S. Pipe Dia 2\"", "1 mtr", 8.000],
                ["B. S. Pipe Dia 2.1/2\"", "1 mtr", 12.000],
                ["B. S. Pipe Dia 3\"", "1 mtr", 16.000],
                ["B.S. Pipe Dia 4\"", "1 mtr", 18.400],
                ["B.S. Pipe Dia 5\"", "1 mtr", 20.000],
                ["B.S. Pipe Dia 6\"", "1 mtr", 24.000],
                ["Ductile Iron Pipe - 4\" (Underground purpose)", "1 mtr", 24.000],
                ["Ductile Iron Pipe - 6\" (Underground purpose)", "1 mtr", 24.000],
                ["UG MS pipe Dia - 4\"", "1 mtr", 28.000],
                ["UG MS pipe Dia - 6\"", "1 mtr", 16.000],
                ["GI Elbow dia 1/2\" to 1.1/2\"", "1 No.", 0.961],
                ["GI Elbow dia 2\" to 3\"", "1 No.", 3.200],
                ["GI Elbow dia 4\" to 6\"", "1 No.", 12.000],
                ["GI Tee dia 1/2\" to 1.1/2\"", "1 No.", 2.000],
                ["GI Tee dia 2\" to 3\"", "1 No.", 4.800],
                ["BSS Tee Dia. 1/2\" to 1.1/2\"", "1 No.", 5.200],
                ["BSS Tee Dia. 2\" to 3\"", "1 No.", 5.600],
                ["BSS Tee Dia. 4\" to 6\"", "1 No.", 12.000],
                ["BSS Elbow Dia 1/2\" to 1.1/2\"", "1 No.", 2.000],
                ["BSS Elbow Dia 2\" to 3\"", "1 No.", 4.800],
                ["BSS Elbow Dia 4\" to 6\"", "1 No.", 8.000],
                ["BSS Flange Dia 3\" to 4\"", "1 No.", 7.200],
                ["BSS Flange Dia 5\" to 6\"", "1 No.", 12.000],
                ["BSS Flange Dia 3\" to 4\" Thread Type", "1 No.", 14.400],
                ["BSS Flange Dia 5\" to 6\" Thread Type", "1 No.", 16.000],
                ["Nut & Bolts 10mm to 18mm Dia Long 60mm", "1 No.", 0.480],
                ["GI Union Dia 1/2\" to 1.1/2\"", "1 No.", 2.400],
                ["GI Union Dia 2\" to 3\"", "1 No.", 6.400],
                ["GI Clamp Socket Dia 4\" with Rubber Gasket", "1 No.", 0.800],
                ["GI Clamp Socket Dia 6\" with Rubber Gasket", "1 No.", 1.200],
                ["Gate Valve Dia 1/2\" to 1.1/2\"", "1 No.", 17.600],
                ["Gate Valve Dia 2\"", "1 No.", 28.000],
                ["Gate Valve Dia 3\"", "1 No.", 60.000],
                ["Gate Valve Dia 4\"", "1 No.", 72.000],
                ["Gate Valve Dia 5\"", "1 No.", 96.000],
                ["Gate Valve Dia 6\"", "1 No.", 128.000],
                ["Butterfly Valve 4\"", "1 No.", 120.000],
                ["Butterfly Valve 6\"", "1 No.", 144.000],
                ["Non-Return Valve 1/2\" to 1.1/2\"", "1 No.", 16.000],
                ["Non-Return Valve 2\" to 3\"", "1 No.", 28.000],
                ["Non-Return Valve 4\" to 6\"", "1 No.", 120.000],
                ["Pressure Relief Valve 1/2\"", "1 No.", 14.400],
                ["Pressure Relief Valve 4\"", "1 No.", 120.000],
                ["Pressure Relief Valve 6\"", "1 No.", 176.000],
                ["Copper type Valve 3/8\" to 1/2\" - 3 way", "1 No.", 25.000],
                ["Copper type Valve 3/8\" to 1/2\" - 4 way", "1 No.", 20.000],
                ["Copper pipe 3/8\" to 1/2\"", "1 mtr", 10.000],
                ["Motor Coupler 500 GPM to 1500 GPM", "1 No.", 415.000],
                ["Shaft 500 GPM to 1500 GPM", "1 No.", 825.000],
                ["Impeller 500 GPM to 1500 GPM", "1 No.", 415.000],
                ["Shaft Sleeve 500 GPM to 1500 GPM", "1 No.", 430.000],
                ["Diesel Engine Filters 500 GPM", "1 No.", 72.000],
                ["Diesel Engine Filters 1000 GPM", "1 No.", 96.000],
                ["Diesel Engine Filters 1500 GPM", "1 No.", 80.000],
                ["Starter for Diesel Engine", "1 No.", 225.000],
                ["Jackey pump 5HP Vertical type", "1 No.", 2450.000],
                ["Mechanical Pump 500 GPM", "1 No.", 4250.000],
                ["Mechanical Pump 1000 GPM", "1 No.", 5650.000],
                ["Mechanical Pump 1500 GPM", "1 No.", 7250.000],
                ["Rewinding of Motor 5HP", "1 No.", 950.000],
                ["Rewinding of Motor 7HP", "1 No.", 1025.000],
                ["Rewinding of motor 10HP", "1 No.", 1145.000],
                ["Rewinding of motor 15HP", "1 No.", 1585.000],
                ["Fan blades for motor 5HP to 7HP", "1 No.", 480.000],
                ["Fan blades for motor 10HP to 15HP", "1 No.", 520.000],
                ["Electrical pump controller panel PCB", "1 No.", 685.000],
                ["Electric pump controller panel switches", "1 No.", 450.000],
                ["Diesel Engine pump controller panel PCB", "1 No.", 485.000],
                ["Diesel Engine pump controller panel switches", "1 No.", 485.000],
                ["Bourdon tube pressure setting Device", "1 No.", 28.000],
                ["Thermostat for Jockey Electrical & Diesel Pump Controller", "1 No.", 425.000],
                ["Jockey pump controller panel PCB", "1 No.", 480.000],
                ["Jockey pump controller panel switches", "1 No.", 450.000],
                ["Contactor", "1 No.", 28.000],
                ["Isolator", "1 No.", 40.000],
                ["Relay", "1 No.", 32.000],
                ["Timer", "1 No.", 52.000],
                ["Battery 100 Ah (for Diesel Engine)", "1 No.", 60.000],
                ["Battery 150 Ah (for Diesel Engine)", "1 No.", 72.000],
                ["Battery 200 Ah (for Diesel Engine)", "1 No.", 80.000],
                ["Compressor Auto Drain Valve 1/2\"", "1 No.", 15.000],
                ["Compressor Auto Drain Valve 3/4\"", "1 No.", 15.000],
                ["Pressure Reducing Valve 1/2\"", "1 No.", 17.600],
                ["Pressure Reducing Valve 3/4\"", "1 No.", 20.000],
                ["Compressor Piston", "1 No.", 96.000],
                ["Compressor piston ring with Different sizes", "1 No.", 44.000],
                ["Drain valve for Compressor in & out", "1 No.", 80.000],
                ["Compressor complete unit for 10 Bar", "1 No.", 750.000],
                ["Deluge valve set", "1 No.", 780.000],
                ["Deluge valve Rubber O-Ring 4\" Dia different Thickness", "1 No.", 20.000],
                ["Deluge valve Rubber O-Ring 6\" Dia different Thickness", "1 No.", 20.000],
                ["Deluge valve piston 4\" Dia", "1 No.", 48.000],
                ["Deluge valve piston 6\" Dia", "1 No.", 68.000],
                ["Deluge valve Disk plate 4\"", "1 No.", 96.000],
                ["Deluge valve Disk plate 6\"", "1 No.", 120.000],
                ["Pressure Gauge Dia 2\" to 15 Bar", "1 No.", 44.000],
                ["Pressure Gauge Dia 4\" to 15 Bar", "1 No.", 68.000],
                ["Pressure Switch", "1 No.", 280.000],
                ["Flow Switch", "1 No.", 120.000],
                ["Level Switch", "1 No.", 96.000],
                ["Water level Indicator", "1 No.", 440.000],
                ["Floating Valve 4\"", "1 No.", 64.000],
                ["Floating Valve 6\"", "1 No.", 120.000],
                ["GRP Tank 50, 000 Gallons", "1 No.", 8650.000],
                ["GRP Tank 30, 000 Gallons", "1 No.", 7500.000],
                ["Single head Fire Hydrant Valve", "1 No.", 280.000],
                ["Double headed Fire Hydrant Valve", "1 No.", 360.000],
                ["Canvas Hose 2\" 30 Mtrs Long with Accessories", "1 No.", 104.000],
                ["Fire Brigade Inlet", "1 No.", 240.000],
                ["Stat -Delta contactor(250A)", "1 No.", 52.000],
                ["MS Strainer-12\"", "1 No.", 360.000],
                ["MS flange", "1 No.", 44.000],
                ["M.S.Vessel Tank", "1 No.", 480.000],
                ["Pressure differential switch,0-12 bar", "1 No.", 640.000],
                ["1\" X 9\",Berrel nipple", "1 No.", 44.000],
                ["Glass fuse,3 A,20 mm", "1 No.", 32.000],
                ["MCCB, 63A,3P", "1 No.", 1.600],
                ["MS Strainer-8\"", "1 No.", 360.000],
                ["Foot valve-8\"", "1 No.", 360.000],
                ["Pressure differential switch,0-12 bar", "1 No.", 480.000],
                ["MS vessel tank", "1 No.", 480.000],
                ["1\" X 9”, Berrel nipple", "1 No.", 20.000],
                ["Glass fuse,3 A,20 mm", "1 No.", 2.400],
                ["ID-6”, MS strainer", "1 No.", 320.000],
                ["MCCB, 63A,3P", "1 No.", 48.000],
                ["ID-8”, Foot valve", "1 No.", 360.000],
                ["1/2\", heavy duty ball valve, Brass", "1 No.", 120.000],
                ["1/2\" X 6\", GI berrel nipple", "1 No.", 20.000],
                ["1/2\" X 4\", GI berrel nipple", "1 No.", 52.000],
                ["3/8 X 1/2\", Reducer", "1 No.", 68.000],
                ["1/2\" X 3\", GI berrel nipple", "1 No.", 68.000],
                ["1/2\" X 6\", GI berrel nipple", "1 No.", 96.000],
                ["1/2\" X 4\", GI berrel nipple", "1 No.", 120.000],
                ["Main Pump Impeller", "1 No.", 960.000],
                ["Fire Hose Reel Cabinet", "1 No.", 120.000],
                ["Silencer with muffler", "1 No.", 1250.000],
                ["5mm rubber gasket", "1 Sq. mtr", 15.000],
                ["Battery terminal cover", "1 No.", 20.000],
                ["NRV-8\"", "1 No.", 440.000],
                ["Steel bolt for underground pipeline flange.", "1 No.", 20.000],
                ["Pressure Transmitter (PT)", "1 No.", 440.000],
                ["Fire Engine controller panel programmer", "1 No.", 400.000],
                ["Battery Charger 12V", "1 No.", 480.000],
                ["Metallic gasket for Deluge Valve", "1 Sq. mtr", 64.000],
                ["ARV (Air release valve) Valmatic,1/2\",CWP 175 PSIG ARV", "1 No.", 200.000],
                ["Grooved Coupling, Size - 6\"", "1 No.", 2.800],
                ["Reducer Bush, Size - 6\" x 4\"", "1 No.", 20.000],
                ["L Angle support", "1 No.", 16.000],
                ["U Bolt for Support", "1 No.", 12.000],
                ["Pressure gauge 300 PSI", "1 No.", 28.000],
                ["Selector Switch", "1 No.", 28.000],
                ["Gland Rope", "1 No.", 60.000],
                ["1/2\" MS Strainer", "1 No.", 44.000],
                ["1\" MS Strainer", "1 No.", 60.000],
                ["1/2\" Coupling", "1 No.", 4.000],
                ["Four Way Valve", "1 No.", 44.000],
                ["Reducer-1\"x1/2\"", "1 No.", 2.400],
                ["1\" End Plug", "1 No.", 16.000],
                ["1/2\" GI Pipe", "1 No.", 0.800],
                ["Reducer, Size 8\"x 6\"", "1 No.", 20.000],
                ["Diesel Engine Fuel Pump", "1 No.", 400.000],
                ["Nipple. 1\"", "1 No.", 4.000],
                ["Coolant tank for diesel engine", "1 No.", 20.000],
                ["35 Sq. mm Cable, 4 Core", "1 mtr", 16.000],
                ["Reducer-10\"x6\"", "1 No.", 200.000],
                ["Grooved Coupling-6\"", "1 No.", 4.800],
                ["Water tank level Indicator", "1 No.", 480.000],
                ["Splider for Electrical motor & Pump", "1 No.", 400.000],
                ["Diesel engine RPM Sensor", "1 No.", 280.000],
                ["GI Reducer", "1 No.", 8.000],
                ["HDPE Pipe, Size - 10\"", "1 mtr", 17.600],
                ["HDPE Tee, Size - 10\"", "1 No.", 52.000],
                ["HDPE Reducer, Size 10\" x 8\"", "1 No.", 52.000],
                ["HDPE Elbow, 90 deg, Size - 8\"", "1 No.", 52.000],
                ["HDPE Reducer, Size 8\" x 6\"", "1 No.", 52.000],
                ["Fire Hydrant end cap", "1 No.", 8.000],
                ["Pressure transducer", "1 No.", 280.000],
                ["Battery Charger-24V", "1 No.", 320.000],
                ["Heavy Duty Exhaust fan (24\") with all accessories required in FFS pump room", "1 No.", 1200.000],
                ["Bellow-1\"", "1 No.", 120.000],
                ["Auto -Off-Hand Switch Auto -Off-Hand Switch", "1 No.", 200.000],
                ["Water pressure control switch", "1 No.", 200.000],
                ["FFS (2'') pipe Painting work", "mtr", 6.000],
                ["FFS (1'') pipe Painting work", "mtr", 6.000],
                ["FFS (1/2'') pipe Painting work", "mtr", 6.000],
                ["FFS (4'') pipe Painting work", "mtr", 6.000],
                ["FFS (6'') pipe Painting work", "mtr", 6.000],
                ["Pressure tank for Fire Fighting System (200Liter pressure vessel)", "1 No.", 960.000],
                ["PCB Card need to replace", "1 No.", 640.000],
                ["Grooved Coupling -4\"", "1 No.", 28.000],
                ["Water Seal for FFS pumps", "1 No.", 544.000],
                ["Bellow-6\"", "1 No.", 224.000],
                ["Fire Hydrant hose reel Jet Nozzle", "1 No.", 96.000],
                ["Diesel Engine-Cylinder Head", "1 No.", 304.000],
                ["Diesel Engine-Piston Kit & ring set", "1 No.", 400.000],
                ["Diesel Engine-Cylinder Liner with O rings", "1 No.", 200.000],
                ["Diesel Engine-Connecting Rod", "1 No.", 240.000],
                ["Diesel Engine-Connecting Rod bearing set", "1 No.", 480.000],
                ["Diesel Engine-Main Bearing set", "1 No.", 1250.000],
                ["Diesel Engine-Thrust bearing cap", "1 No.", 220.000],
                ["Diesel Engine-Full Engine Gasket Set", "1 No.", 325.000],
                ["Diesel Engine-Water Pump Service Kit assembly", "1 No.", 245.000],
                ["Diesel Engine-Cylinder Head Service plug Kits", "1 No.", 475.000],
                ["Diesel Engine-Oil cooler & Service Kit", "1 No.", 100.000],
                ["Diesel Engine-Fuel Injectors", "1 No.", 100.000],
                ["Diesel Engine-Exhaust Valve", "1 No.", 315.000],
                ["Diesel Engine-Inlet Valve", "1 No.", 245.000],
                ["Diesel Engine-Exhaust Valve spring", "1 No.", 245.000],
                ["Diesel Engine-Inlet Valve spring", "1 No.", 245.000],
                ["Diesel Engine-Valve Guide collet", "1 No.", 200.000],
                ["Diesel Engine-Push Rod", "1 No.", 345.000],
                ["Diesel Engine Coolant Tank", "1 No.", 565.000],
                ["Diesel Engine-Y 4100-Parts cylinder liners", "1 No.", 385.000],
                ["Diesel Engine-large End Bearing Set", "Set", 245.000],
                ["Diesel Engine-Engine Gasket set", "Set", 230.000],
                ["Diesel Engine-Radiator Fan", "1 No.", 230.000],
                ["Diesel Engine-Piston (With Pin)", "1 No.", 265.000],
                ["Diesel Engine-Piston ring set - RE507852", "Set", 240.000],
                ["Liner O Ring Set - AR 65507", "Set", 120.000],
                ["Solenoid Valve", "1 No.", 150.000],
                ["50Kg DCP type Fire Extinguisher", "1 No.", 120.000],
                ["Fire Extinguisher Refilling charges", "1 No.", 75.000],
                ["Total", "", 0]
            ]
            frm.clear_table("ff_systems_spare_parts");
            ffPartsData.forEach(([ description,uom,unit_price]) => {
                let row = frm.add_child("ff_systems_spare_parts");
                row.unit_price = unit_price;
                row.description = description;
                row.uom = uom;
            });
            frm.refresh_field("ff_systems_spare_parts");
        }
        function add_or_move_total(frm, table_name) {
            let table = frm.doc[table_name];

            // Find index of existing Total row (if any)
            let total_index = table.findIndex(row => row.description === "Total");

            let total_row;

            if (total_index === -1) {
                total_row = frm.add_child(table_name);
                total_row.description = "Total";
                total_row.read_only_row = 1;    
            } else {
                total_row = table.splice(total_index, 1)[0];
                total_row.read_only_row = 0;    
            }

            table.push(total_row);

            frm.refresh_field(table_name);
        }


    // Apply to all tables
    add_or_move_total(frm, "base_manpower");
    add_or_move_total(frm, "airconditioning_system_spare_parts");
    add_or_move_total(frm, "ff_systems_spare_parts");


        const grid_pm = frm.fields_dict.base_manpower?.grid;

        if (grid_pm && grid_pm.grid_rows.length) {
            const last_row_pm = grid_pm.grid_rows[grid_pm.grid_rows.length - 1];

            last_row_pm.wrapper.css('background-color', '#f2f2f2');

            frm.doc.base_manpower.forEach(row => {
                if (row.idx === frm.doc.base_manpower.length) {
                    frappe.model.set_value(row.doctype, row.name, "read_only_row", 1);
                }
            });
        }
        const grid_acc = frm.fields_dict.base_vehicle?.grid;

        if (grid_acc && grid_acc.grid_rows.length) {
            const last_row_acc = grid_acc.grid_rows[grid_acc.grid_rows.length - 1];

            last_row_acc.wrapper.css('background-color', '#f2f2f2');

            frm.doc.base_vehicle.forEach(row => {
                if (row.idx === frm.doc.base_vehicle.length) {
                    frappe.model.set_value(row.doctype, row.name, "read_only_row", 1);
                }
            });
        }
        const table_3 = frm.fields_dict.base_vehicle_cost_per_trip?.grid;

        if (table_3 && table_3.grid_rows.length) {
            const last_row_t3 = table_3.grid_rows[table_3.grid_rows.length - 1];

            last_row_t3.wrapper.css('background-color', '#f2f2f2');

            frm.doc.base_vehicle_cost_per_trip.forEach(row => {
                if (row.idx === frm.doc.base_vehicle_cost_per_trip.length) {
                    frappe.model.set_value(row.doctype, row.name, "read_only_row", 1);
                }
            });
        }
        const table_4 = frm.fields_dict.airconditioning_system_spare_parts?.grid;

        if (table_4 && table_4.grid_rows.length) {
            const last_row_t4 = table_4.grid_rows[table_4.grid_rows.length - 1];

            last_row_t4.wrapper.css('background-color', '#f2f2f2');

            frm.doc.airconditioning_system_spare_parts.forEach(row => {
                if (row.idx === frm.doc.airconditioning_system_spare_parts.length) {
                    frappe.model.set_value(row.doctype, row.name, "read_only_row", 1);
                }
            });
        }
        const table_5 = frm.fields_dict.ff_systems_spare_parts?.grid;

        if (table_5 && table_5.grid_rows.length) {
            const last_row_t5 = table_5.grid_rows[table_5.grid_rows.length - 1];

            last_row_t5.wrapper.css('background-color', '#f2f2f2');

            frm.doc.ff_systems_spare_parts.forEach(row => {
                if (row.idx === frm.doc.ff_systems_spare_parts.length) {
                    frappe.model.set_value(row.doctype, row.name, "read_only_row", 1);
                }
            });
        }
        
        
        
    },
    invoice_from(frm) {
        if (frm.doc.invoice_from && frm.doc.invoice_upto) {
            if (frm.doc.invoice_from > frm.doc.invoice_upto) {
                frm.set_value('invoice_from', '');
                frappe.throw('Invoice From date cannot be greater than Invoice Upto Date');
            } else {
            const fromDate = frappe.datetime.str_to_obj(frm.doc.invoice_from);
            const toDate = frappe.datetime.str_to_obj(frm.doc.invoice_upto);
            const diffTime = toDate.getTime() - fromDate.getTime();
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1; 

            const tables = ["base_vehicle", "base_manpower"];
            tables.forEach(table => {
                frm.doc[table].forEach(row => {
                    row.no_of_days = diffDays;
                });
                frm.refresh_field(table);
            });
        }
        }
    },
    

    invoice_upto(frm){
        if (frm.doc.invoice_from && frm.doc.invoice_upto){
            if (frm.doc.invoice_from > frm.doc.invoice_upto){
                frm.set_value('invoice_upto','')
                frappe.throw('Invoice Upto Date must be greater than Invoice from date')
            }else {
            const fromDate = frappe.datetime.str_to_obj(frm.doc.invoice_from);
            const toDate = frappe.datetime.str_to_obj(frm.doc.invoice_upto);
            const diffTime = toDate.getTime() - fromDate.getTime();
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1; 

            const tables = ["base_vehicle", "base_manpower"];
            tables.forEach(table => {
                frm.doc[table].forEach(row => {
                    row.no_of_days = diffDays;
                });
                frm.refresh_field(table);
            });
        }
        }
    },
    month(frm) {
        set_invoice_dates_and_update_rows(frm);
    },
    year(frm) {
        set_invoice_dates_and_update_rows(frm);
    }
});

function set_invoice_dates_and_update_rows(frm) {
    const monthMap = {
        Jan: 0, Feb: 1, Mar: 2, Apr: 3, May: 4, Jun: 5,
        Jul: 6, Aug: 7, Sep: 8, Oct: 9, Nov: 10, Dec: 11
    };

    const month = frm.doc.month;
    const year = frm.doc.year;

    if (month && year && monthMap.hasOwnProperty(month)) {
        const monthIndex = monthMap[month];

        const fromDate = new Date(year, monthIndex, 1);
        const toDate = new Date(year, monthIndex + 1, 0); 

        frm.set_value('invoice_from', frappe.datetime.obj_to_str(fromDate));
        frm.set_value('invoice_upto', frappe.datetime.obj_to_str(toDate));

        
    }else{
        frm.set_value('invoice_from', '');
        frm.set_value('invoice_upto', '');

    }
}

frappe.ui.form.on('Permanent Manpower', {
	
	employees_provided(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.employees_provided>0 && row.unit_price > 0){
            row.total_claim_this_month = row.employees_provided*row.unit_price
            row.amount_to_be_paid=row.total_claim_this_month
		    frm.refresh_field('base_manpower')
        }
		
	},
    no_of_absent(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.no_of_absent>0 && row.unit_price > 0){
            row.deduction_for_absent= row.unit_price/row.no_of_days*row.no_of_absent
            if (row.penalty_for_absent > 0){
                tot=row.penalty_for_absent+row.deduction_for_absent
            }else{
                tot=row.deduction_for_absent
            }
            row.total_deduction= tot
            row.amount_to_be_paid= row.amount_to_be_paid-tot
            frm.refresh_field('base_manpower')
        }
		
	},
    deduction_for_absent(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.deduction_for_absent>0){
            if (row.penalty_for_absent > 0){
                tot=row.penalty_for_absent+row.deduction_for_absent
            }else{
                tot=row.deduction_for_absent
            }
            row.total_deduction= tot
            row.amount_to_be_paid= row.amount_to_be_paid-tot
            frm.refresh_field('base_manpower')

        }
		
	},
    penalty_for_absent(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.penalty_for_absent>0){
            if (row.deduction_for_absent > 0){
                tot=row.penalty_for_absent+row.deduction_for_absent
            }else{
                tot=row.penalty_for_absent
            }
            row.total_deduction= tot
            row.amount_to_be_paid= row.amount_to_be_paid-tot
            frm.refresh_field('base_manpower')

        }
		
	},
	
})

frappe.ui.form.on('Permanent Vehicle', {
	
	total_provided(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_provided>0 && row.unit_price > 0){
            row.total_claim_this_month = row.total_provided*row.unit_price
            row.amount_to_be_paid=row.total_claim_this_month
		    frm.refresh_field('base_vehicle')
        }
		
	},
    days_of_unavailability(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.days_of_unavailability>0 && row.unit_price > 0){
            row.deduction= row.unit_price/row.no_of_days*row.days_of_unavailability
            if (row.penalty > 0){
                tot=row.penalty+row.deduction
            }else{
                tot=row.deduction
            }
            row.total_deduction= tot
            row.amount_to_be_paid= row.amount_to_be_paid-tot
            frm.refresh_field('base_vehicle')
        }
		
	},
    deduction(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.deduction>0){
            if (row.penalty > 0){
                tot=row.penalty+row.deduction
            }else{
                tot=row.deduction
            }
            row.total_deduction= tot
            row.amount_to_be_paid= row.amount_to_be_paid-tot
            frm.refresh_field('base_vehicle')

        }
		
	},
    penalty(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.penalty>0){
            if (row.deduction > 0){
                tot=row.penalty+row.deduction
            }else{
                tot=row.penalty
            }
            row.total_deduction= tot
            row.amount_to_be_paid= row.amount_to_be_paid-tot
            frm.refresh_field('base_vehicle')

        }
		
	},
    
	
})

frappe.ui.form.on('Base Vehicle Cost Per Trip', {
	no_of_trip(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.no_of_trip>0){
           row.total_claim_this_month=row.unit_price*row.no_of_trip
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction

        }else{
            row.amount_to_be_paid= 0

        }
        frm.refresh_field('base_vehicle_cost_per_trip')
	},
		
    total_deduction(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_deduction>0){
           
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction

        }else{
            row.amount_to_be_paid= row.total_claim_this_month

        }
        frm.refresh_field('base_vehicle_cost_per_trip')
	},
    total_claim_this_month(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_deduction>0){
           
            row.total_deduction= tot
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction
            frm.refresh_field('base_manpower')

        }else{
            row.amount_to_be_paid= row.total_claim_this_month

        }
        frm.refresh_field('base_vehicle_cost_per_trip')

	},
	
})

frappe.ui.form.on('AIRCONDITIONING SYSTEM SPARE PARTS', {
	unit_qty(frm,cdt,cdn){
        var row = locals[cdt][cdn];
        if (row.unit_qty > 0){
            row.total_claim_this_month=row.unit_price*row.unit_qty
            if (row.deduction > 0){
                row.amount_to_be_paid=row.total_claim_this_month-row.deduction
            }else{
                row.amount_to_be_paid=row.total_claim_this_month
            }
        }else{
            row.total_claim_this_month=0
            row.amount_to_be_paid=0
        }
        frm.refresh_field('airconditioning_system_spare_parts')
    },
	unit_price(frm,cdt,cdn){
        var row = locals[cdt][cdn];
        if (row.unit_qty > 0 && row.unit_price > 0){
            row.total_claim_this_month=row.unit_price*row.unit_qty
        }else{
            row.total_claim_this_month=0
        }
        frm.refresh_field('airconditioning_system_spare_parts')
    },
    total_deduction(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_deduction>0){
           
            row.total_deduction= tot
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction
            frm.refresh_field('airconditioning_system_spare_parts')

        }else{
            row.amount_to_be_paid= row.total_claim_this_month

        }
		
	},
    total_claim_this_month(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_deduction>0){
           
            row.total_deduction= tot
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction
            frm.refresh_field('airconditioning_system_spare_parts')

        }else{
            row.amount_to_be_paid= row.total_claim_this_month

        }
		
	},
	
})

frappe.ui.form.on('FF Systems Spare Parts', {
	unit_qty(frm,cdt,cdn){
        var row = locals[cdt][cdn];
        if (row.unit_qty > 0){
            row.total_claim_this_month=row.unit_price*row.unit_qty
        }else{
            row.total_claim_this_month=0
        }
        frm.refresh_field('ff_systems_spare_parts')

    },
	unit_price(frm,cdt,cdn){
        var row = locals[cdt][cdn];
        if (row.unit_qty > 0 && row.unit_price > 0){
            row.total_claim_this_month=row.unit_price*row.unit_qty
        }else{
            row.total_claim_this_month=0
        }
        frm.refresh_field('ff_systems_spare_parts')

    },
    total_deduction(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_deduction>0){
           
            row.total_deduction= tot
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction
            frm.refresh_field('ff_systems_spare_parts')

        }else{
            row.amount_to_be_paid= row.total_claim_this_month
            frm.refresh_field('ff_systems_spare_parts')
        }
		
	},
    total_claim_this_month(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_deduction>0){
           
            row.total_deduction= tot
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction
            frm.refresh_field('ff_systems_spare_parts')

        }else{
            row.amount_to_be_paid= row.total_claim_this_month
            frm.refresh_field('ff_systems_spare_parts')
        }
		
	},
	
})