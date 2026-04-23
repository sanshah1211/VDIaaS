import React, { useState } from "react";
import api from "../services/api";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { AuthLayout } from '../components/javascript/auth-layout';
import { Button } from '../components/javascript/button';
import { Checkbox, CheckboxField } from '../components/javascript/checkbox';
import { Field, Label } from '../components/javascript/fieldset';
import { Heading } from '../components/javascript/heading';
import { Input } from '../components/javascript/input';
import { Strong, Text, TextLink } from '../components/javascript/text';
import { useNavigate } from "react-router-dom";
import Logo from '../assets/ocore.png';


function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
        username: "",
        password: ""
    });
    const handleChange = (e) => {
        setFormData({
            ...formData, [e.target.name]: e.target.value
        });
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post("/", formData);
            if (response.data.message === "Login Success") {
                toast.success(response.data.message);
                console.log(response.data.cookie);
                if (formData.username === "akadmin") {
                    setTimeout(() => {
                        navigate("/admin");
                    }, 1000);
                }
            } else {
                toast.error(response.data.message);
            }
            console.log(response.data);
            setFormData({
                username: "",
                password: ""
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
                toast.error("Login failed");
            }
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-950">
              <ToastContainer
                  position="top-right"
                  autoClose={10000} hideProgressBar={false}
                  newestOnTop
                  closeOnClick
                  pauseOnHover
              />
                <div className="grid grid-cols-5 gap-6 items-center justify-center min-h-screen">
                <div className="col-start-1 col-span-3 pb-15">
                    <img src="../../public/vdi.png" className="w-full max-w-3xl drop-shadow-2xl"/>
                    <p className="text-5xl font-semibold text-blue-200 -mt-5 mr-12 text-center fa-font-awesome-logo-full"> Secure Cloud VDI Platform </p>
                    <div className="flex items-center justify-center gap-1 mt-2 mr-12 text-blue-200  text-2xl">
                        <span>Powered by</span>
                        <img src="../../public/proxmox-full-lockup-inverted-color.svg" alt="Proxmox" className="h-10 opacity-70"/>
                    </div>
                </div>
                <div className="col-span-2 col-end-6 items-center">
                <AuthLayout>
                    <form method="POST" onSubmit={handleSubmit} className="grid w-full max-w-sm grid-cols-1 gap-6 ">
                        <img src={Logo} alt="Logo" className="h-14 -mt-8 justify-start"/>
                        <p className="w-full text-3xl font-semibold text-left whitespace-nowrap text-gray-800"> Sign in to your workspace </p>
                        <Field>
                            <Label>Username</Label>
                            <Input name="username" placeholder="username" value={formData.username} type="text" onChange={handleChange} required />
                        </Field>
                        <Field>
                            <Label>Password</Label>
                            <Input name="password" placeholder="password" value={formData.password} type="password" onChange={handleChange} required />
                        </Field>
                        <div className="flex items-center justify-between">
                            <CheckboxField>
                                <Checkbox name="remember" />
                                <Label>Remember me</Label>
                            </CheckboxField>
                            <Text>
                                <TextLink href="#">
                                    <Strong>Forgot password?</Strong>
                                </TextLink>
                            </Text>
                        </div>
                        <button type="submit" className="button-text-color w-full items-center bg-slate-800 hover:bg-slate-900" >Login</button>
                    </form>
                </AuthLayout>
                </div>
            </div>
        </div>
    );
}
export default Login;