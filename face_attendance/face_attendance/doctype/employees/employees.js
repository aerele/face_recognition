// Copyright (c) 2023, Vignesh P and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employees", {
  refresh: function (frm) {
    let emp_no;

    emp_no = Math.floor(Math.random() * (20000 - 10000 + 1) + 10000);

    if (
      frm.doc.first_name != "" &&
      frm.doc.last_name != "" &&
      frm.doc.gender != "" &&
      frm.doc.date_of_joining != ""
    ) {
      frm.set_value("employee_number", emp_no);
    }
  },

  after_save: function (frm) {
    let full_name = frm.doc.first_name + " " + frm.doc.last_name;
    frm.set_value("full_name", full_name);
  },
});
