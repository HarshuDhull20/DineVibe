import { useState } from "react";
import "../styles/dashboard.css";

export default function Staff() {
  const [staffList, setStaffList] = useState([
    {
      id: 1,
      name: "Rahul Verma",
      role: "Manager",
      email: "rahul@dinevibe.com",
      status: "active",
    },
    {
      id: 2,
      name: "Sneha Kapoor",
      role: "Cashier",
      email: "sneha@dinevibe.com",
      status: "active",
    },
    {
      id: 3,
      name: "Arjun Reddy",
      role: "Reception",
      email: "arjun@dinevibe.com",
      status: "inactive",
    },
  ]);

  const toggleStatus = (id) => {
    setStaffList((prev) =>
      prev.map((staff) =>
        staff.id === id
          ? {
              ...staff,
              status: staff.status === "active" ? "inactive" : "active",
            }
          : staff
      )
    );
  };

  const removeStaff = (id) => {
    setStaffList((prev) => prev.filter((staff) => staff.id !== id));
  };

  return (
    <div className="dashboard-content">

      <h2 className="page-title">Staff Management</h2>

      <div style={{ marginBottom: "20px" }}>
        <button className="primary-btn">+ Add Staff</button>
      </div>

      <div className="section-card">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {staffList.map((staff) => (
              <tr key={staff.id}>
                <td>{staff.name}</td>
                <td>{staff.email}</td>
                <td>{staff.role}</td>
                <td>
                  <span
                    className={`badge ${
                      staff.status === "active"
                        ? "success"
                        : "error"
                    }`}
                  >
                    {staff.status}
                  </span>
                </td>
                <td>
                  <button
                    className="small-btn confirm"
                    onClick={() => toggleStatus(staff.id)}
                  >
                    {staff.status === "active"
                      ? "Deactivate"
                      : "Activate"}
                  </button>

                  <button
                    className="small-btn cancel"
                    onClick={() => removeStaff(staff.id)}
                  >
                    Remove
                  </button>
                </td>
              </tr>
            ))}

            {staffList.length === 0 && (
              <tr>
                <td colSpan="5" style={{ textAlign: "center" }}>
                  No staff members found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

    </div>
  );
}
