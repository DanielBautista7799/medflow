-- hospitals

INSERT INTO hospitals (id, name, location_region, capacity, supervisor_id) VALUES
(1, 'Halcyon Medical Center', 'Central', 450, 101),
(2, 'Northside Community Hospital', 'North', 275, 102),
(3, 'Southpoint Outpatient Center', 'South', 150, 103),
(4, 'Westview Regional Hospital', 'West', 325, 104);

SELECT setval('hospitals_id_seq', (SELECT MAX(id) FROM hospitals));


-- equipment

INSERT INTO equipment
(id, serial_number, model, status, charge_level, facility_id) VALUES
(1, 'PUMP-1001', 'InfusePro X2', 'Available', 85.00, 1),
(2, 'PUMP-1002', 'InfusePro X2', 'In-Use', 15.50, 1),
(3, 'VENT-2001', 'AirFlow V5', 'In-Use', 72.00, 2),
(4, 'VENT-2002', 'AirFlow V5', 'Maintenance', 10.00, 2),
(5, 'MON-3001', 'VitalWatch M3', 'Available', 95.00, 3),
(6, 'MON-3002', 'VitalWatch M3', 'In-Use', 18.25, 3),
(7, 'IMG-4001', 'MobileScan C1', 'Maintenance', 45.00, 4),
(8, 'PUMP-1003', 'InfusePro X2', 'Offline', 5.00, 4);

SELECT setval('equipment_id_seq', (SELECT MAX(id) FROM equipment));


-- Work orders

INSERT INTO work_orders
(id, title, priority, status, equipment_id, technician_id) VALUES
(1, 'Inspect low charge infusion pump', 'Critical', 'Pending', 2, 201),
(2, 'Ventilator preventive maintenance', 'Medium', 'In-Progress', 4, 202),
(3, 'Patient monitor inspection', 'Low', 'Completed', 5, 203),
(4, 'Repair mobile imaging cart', 'Critical', 'Failed', 7, 204),
(5, 'Inspect low charge monitor', 'Medium', 'Pending', 6, 201),
(6, 'Infusion pump diagnostic', 'Critical', 'Completed', 1, 202);

SELECT setval('work_orders_id_seq', (SELECT MAX(id) FROM work_orders));


-- service Reports

INSERT INTO service_reports
(id, work_order_id, file_url, notes, created_at) VALUES
(1, 3, 'reports/monitor-3001-inspection.pdf', 'Inspection completed successfully.', NOW()),
(2, 4, 'reports/img-4001-diagnostic.txt', 'Imaging cart requires additional repair.', NOW()),
(3, 6, 'reports/pump-1001-diagnostic.pdf', 'Diagnostic completed with no major issues.', NOW());

SELECT setval('service_reports_id_seq', (SELECT MAX(id) FROM service_reports));