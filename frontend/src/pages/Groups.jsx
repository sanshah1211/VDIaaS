import Dashboard from "../components/Layout/Dashboard"
import React, { useState } from "react";
import api from "../services/api";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
{/*import { useNavigate } from "react-router-dom";*/}

function Groups() {
      {/*const navigate = useNavigate();*/}
      const [openDialog, setOpenDialog] = useState(false);
      const [groups, setGroups] = useState([]);
      const [loaded, setLoaded] = useState(false);
      const [formData, setFormData] = useState({
        group: ""
      });

      {/* Fetch Group Data for Table */}
      const fetchGroups = async () => {
          try {
              const response = await api.get("/groups");
              setGroups(response.data.group_details);
          } catch {
              toast.info("No Groups Available to Display");
          }
      };
    {/* Page Content Loading */}
      if (!loaded) {
          setLoaded(true);
          fetchGroups();
      }
    {/* Save Input Data */}
      const handleChange = (e) => {
        setFormData({
            ...formData, [e.target.name]: e.target.value
        });
      };

    {/* Button On Click event */}
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post("/create-groups", formData);
            if (response.data.message === "Group Created") {
                toast.success(response.data.message);
                setOpenDialog(false);
                fetchGroups();
            } else {
                toast.error(response.data.message);
            }
            console.log(response.data);
            setFormData({
                group: "",
            });
        } catch (error) {
            if (error.response && error.response.data) {
                const msg = error.response.data.message;
                if (typeof msg === "object") {
                    const formatted = Object.entries(msg)
                        .map(([field, errors]) => `${field}: ${errors.join(", ")}`)
                        .join(" | ");
                    toast.error(formatted);
                } else {
                    toast.error(msg);
                }
            } else {
                toast.error("Group Creation Failed");
            }
        }
    };

    {/* Delete Groups */}
    const handleDelete = async (group_name) => {
        if (!window.confirm(`Delete group "${group_name}"?`)) return;
            try {
                const response = await api.delete(`/delete-groups/${group_name}`);
                if (response.data.message === "Group Deleted") {
                    toast.success(response.data.message);
                    setOpenDialog(false);
                    fetchGroups();
                } else {
                    toast.error(response.data.message);
                }
                console.log(response.data);
                setFormData({
                    group: "",
                });
            } catch (error) {
                if (error.response && error.response.data) {
                    const msg = error.response.data.message;
                    if (typeof msg === "object") {
                        const formatted = Object.entries(msg)
                            .map(([field, errors]) => `${field}: ${errors.join(", ")}`)
                            .join(" | ");
                            toast.error(formatted);
                    } else {
                        toast.error(msg);
                    }
                } else {
                    toast.error("Group Deletion Failed");
                }
            }
        };

    return (
      <Dashboard>
          <ToastContainer position="top-right" autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick pauseOnHover/>
          <div className="relative flex flex-col w-full h-full text-slate-700 bg-white  rounded-xl">
              <div className="relative mx-4 mt-4 overflow-hidden text-slate-700 bg-white rounded-none">
                  <div className="flex items-center justify-between ">
                      <div>
                          <h3 className="text-xl font-semibold text-slate-800">User Group Details</h3>
                      </div>
                      <div className="flex flex-col gap-2 shrink-0 sm:flex-row">
                           <button onClick={() => setOpenDialog(true)}
                              className="button-text-color flex select-none items-center gap-2 rounded-md bg-slate-800 py-2.5 px-4 text-xl font-semibold text-white shadow-md shadow-slate-900/10 transition-all hover:shadow-lg hover:shadow-slate-900/20 focus:opacity-[0.85] focus:shadow-none active:opacity-[0.85] active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
                              type="submit">
                              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 22" fill="currentColor"
                                   aria-hidden="true"
                                   stroke-width="2" className="w-4 h-4">
                                  <path d="M12 5v14m-7-7h14" stroke="currentColor" strokeWidth="4" strokeLinecap="round"/>
                              </svg>
                          </button>
                      </div>
                  </div>
              </div>
              {/* Table Format */}
              <div className="bg-white mt-4 rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                  <table className="w-full text-left table-auto">
                      {/* HEADER */}
                      <thead className="bg-slate-50">
                      <tr>
                          {["Group Name", "Users", "Roles", "Action"].map((title, i) => (
                              <th key={i} className="p-4 text-sm font-semibold text-slate-600 border-b border-slate-200">
                                  <div className="flex items-center justify-between">
                                      {title}
                                      {title !== "Action" && (
                                          <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                              <form action=""></form>
                                              <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 15L12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9"/>
                                          </svg>
                                      )}
                                  </div>
                              </th>
                          ))}
                      </tr>
                      </thead>
                      {/* BODY */}
                      <tbody>
                      {groups.map((group, index) => (
                          <tr key={index} className="hover:bg-slate-50 transition-colors">
                              {/* Group Name */}
                              <td className="p-4 border-b border-slate-100">
                                  <p className="text-sm font-medium text-slate-800">
                                      {group.group_name}
                                  </p>
                              </td>
                              {/* Users */}
                              <td className="p-4 border-b border-slate-100">
                                  {group.users && group.users.length > 0 ? (
                                      <div className="flex flex-wrap gap-2">
                                          {[...new Set(group.users)].map((user, i) => (
                                              <span key={i} className="px-2 py-1 text-xs bg-slate-100 text-slate-600 rounded-md">
                                                  {user}
                                              </span>
                                          ))}
                                      </div>
                                  ) : (
                                      <span className="text-sm text-slate-400 italic"> No users assigned </span>
                                  )}
                              </td>
                              {/* Roles */}
                              <td className="p-4 border-b border-slate-100">
                                  {group.roles && group.roles.length > 0 ? (
                                      <div className="flex flex-wrap gap-2">
                                          {[...new Set(group.roles)].map((role, i) => (
                                              <span key={i} className="px-2 py-1 text-xs bg-blue-50 text-blue-600 rounded-md">
                                                  {role}
                                              </span>
                                          ))}
                                      </div>
                                  ) : (
                                      <span className="text-sm text-slate-400 italic">
                                          No roles assigned
                                      </span>
                                  )}
                              </td>
                              {/* Actions */}
                              <td className="p-4 border-b border-slate-100">
                                  <button onClick={() => handleDelete(group.group_name)} className="p-2 rounded-md hover:bg-red-50 text-slate-500 hover:text-red-600 transition">
                                      <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                                          <path d="M9 3a1 1 0 00-1 1v1H5a1 1 0 000 2h.293l.854 10.243A2 2 0 008.14 19h7.72a2 2 0 001.993-1.757L18.707 7H19a1 1 0 100-2h-3V4a1 1 0 00-1-1H9z" />
                                      </svg>
                                  </button>
                              </td>
                          </tr>
                      ))}
                      </tbody>
                  </table>
              </div>
              <div className="flex items-center justify-between p-3">
                  <p className="block text-sm text-slate-500"> Page 1 of 10</p>
                  <div className="flex gap-1">
                      <button className="rounded border border-slate-300 py-2.5 px-3 text-center text-xs font-semibold text-slate-600 transition-all hover:opacity-75 focus:ring focus:ring-slate-300 active:opacity-[0.85] disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" type="button">
                          Previous
                      </button>
                      <button className="rounded border border-slate-300 py-2.5 px-3 text-center text-xs font-semibold text-slate-600 transition-all hover:opacity-75 focus:ring focus:ring-slate-300 active:opacity-[0.85] disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" type="button">
                          Next
                      </button>
                  </div>
              </div>
          </div>
          {openDialog && (
          <div data-dialog-backdrop="dialog" data-dialog-backdrop-close="true" className="absolute left-0 top-0 inset-0 z-[999] grid place-items-center bg-transparent backdrop-blur-xs transition-opacity duration-300">
              <div data-dialog="dialog" className="relative mx-auto flex w-full max-w-[24rem] flex-col rounded-xl text-slate-700 bg-clip-border bg-slate-300/60  border-slate-900 border-2 shadow-md">
                  <button onClick={() => setOpenDialog(false)} className="absolute top-4 right-3 text-slate-700 hover:text-slate-900">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 hover:stroke-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={4}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                  </button>
                  <div className="flex flex-col p-6">
                      <h4 className="text-2xl mb-3 font-semibold text-slate-700"> Create New Group </h4>
                      <p className="mb-1 mt-1 text-shadow-slate-700"> Enter information to create groups.</p>
                      <div className="w-full max-w-sm min-w-[200px] mt-4">
                          <label className="block mb-2 text-md font-semibold text-shadow-slate-700">
                              Group Name
                          </label>
                          <input name="group" type="text" className="w-full h-10 bg-transparent placeholder:text-shadow-slate-800 text-slate-800 text-sm border border-slate-400 rounded px-3 py-2 transition duration-300 ease focus:outline-none focus:border-slate-700 hover:border-slate-900 shadow-sm focus:shadow-md" placeholder="group" value={formData.group} onChange={handleChange} required/>
                      </div>
                  </div>
                  <div className="p-6 pt-0">
                      <div className="flex space-x-2">
                         <button
                              className="button-text-color w-full mx-auto select-none rounded bg-slate-800 py-2 px-4 text-center text-sm font-semibold text-white shadow-md shadow-slate-900/10 transition-all hover:shadow-lg hover:shadow-slate-900/20 active:opacity-[0.85] disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
                              type="button"
                              data-dialog-close="true" onClick={handleSubmit}>
                              Create
                         </button>
                           <button onClick={() => setOpenDialog(false)}
                              className="border-button w-full rounded-md ml-2 text-slate-800 text-sm border-2 border-slate-800 rounded px-3 py-2"
                              type="button"
                              data-dialog-close="true">
                              Cancel
                          </button>
                      </div>
                  </div>
              </div>
          </div>)}
      </Dashboard>
    );
}

export default Groups;