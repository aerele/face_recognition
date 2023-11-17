// Copyright (c) 2023, Vignesh P and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Check', {
	// refresh: function(frm) {

	// }
	click_for_attendence: function (frm) {
		// const scanner = new frappe.ui.Scanner({
		//   dialog: true, // open camera scanner in a dialog
		//   multiple: false, // stop after scanning one value
		//   on_scan(data) {
		//     handle_scanned_barcode(data.decodedText);
		//   }
		// });
		
		console.log("Before save hook triggered");
		frappe.call({
		  method:
			"face_attendance.face_attendance.doctype.employee_check.employee_check.picture_for_verification",
		  args: {
			check: frm.doc.image_for_verification,
			name: frm.doc.employee_name
		  },
		  callback: function (r) {
			if (r.message) {
			  frappe.msgprint(r.message);
			}
		  },
		});
	  },
	
	
});
