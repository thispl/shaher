// frappe.ui.form.on('Mark Attendance', {
//     // onload: function(frm) {
//     //     // Hide submit button if the user is not an HOD
//     //     frappe.call({
//     //         method: 'shaher.shaher.doctype.mark_attendance.mark_attendance.is_hod',
//     //         args: { user: frappe.session.user },
//     //         callback: function(response) {
//     //             if (!response.message) {
//     //                 frm.disable_save();
//     //                 frappe.msgprint(__('Only HOD can submit this document.'));
//     //             }
//     //         }
//     //     });
//     // },

//     before_submit: function(frm) {
//         frappe.call({
//             method: 'shaher.shaher.doctype.mark_attendance.mark_attendance.is_hod',
//             args: { user: frappe.session.user },
//             async: false,
//             callback: function(response) {
//                 if (!response.message) {
//                     frappe.throw(__('Only HOD can submit this document.'));
//                 }
//             }
//         });

//         // Ensure In Time and Out Time are set before submission
//         if (!frm.doc.in_time || !frm.doc.out_time) {
//             frappe.throw(__('Both In Time and Out Time must be set before submission.'));
//         }
//     },

//     // after_submit: function(frm) {
//     //     frappe.call({
//     //         method: 'shaher.shaher.doctype.mark_attendance.mark_attendance.create_checkins',
//     //         args: {
//     //             employee: frm.doc.employee,
//     //             in_time: frm.doc.in_time,
//     //             out_time: frm.doc.out_time
//     //         },
//     //         callback: function(response) {
//     //             if (response.message) {
//     //                 frappe.msgprint(__('Check-ins created successfully.'));
//     //             }
//     //         }
//     //     });
//     // }
// });
