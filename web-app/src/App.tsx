import { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from "./components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { Badge } from "./components/ui/badge";
import { Separator } from "./components/ui/separator";
import { Skeleton } from "./components/ui/skeleton";
import { LucideSparkles, LucideBriefcase, LucideUpload, LucideCheckCircle, LucideGlobe } from 'lucide-react';

// Types based on backend pydantic models
interface JobRole {
    role: string;
    experience_level: string;
    skills: string[];
    responsibilities: string[];
    qualifications: string[];
}

interface AnalysisResult {
    experience_level: string;
    skill_match: string;
    final_decision: string;
    screened_for_role: string;
}

const BACKEND_URL = "http://127.0.0.1:8000";

function App() {
    const [jobRole, setJobRole] = useState<JobRole | null>(null);
    const [generatingRole, setGeneratingRole] = useState(false);
    const [file, setFile] = useState<File | null>(null);
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [loadingTime, setLoadingTime] = useState(0);

    // Fetch a random job role on mount
    useEffect(() => {
        fetchNewJobRole();
    }, []);

    const fetchNewJobRole = async () => {
        setGeneratingRole(true);
        setJobRole(null);

        try {
            const resp = await axios.post(`${BACKEND_URL}/generate-job-role`);
            setJobRole(resp.data);
            setResult(null);
            setFile(null);
        } catch (e) {
            console.error("Failed to fetch job role", e);
        } finally {
            setGeneratingRole(false);
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleSubmit = async () => {
        if (!file || !jobRole) return;

        setLoading(true);
        setResult(null);
        setLoadingTime(0);

        const timerInterval = setInterval(() => {
            setLoadingTime(prev => prev + 1);
        }, 1000);

        try {
            const formData = new FormData();
            formData.append("file", file);
            formData.append("job_role", jobRole.role);

            const MIN_WAIT_MS = 60000;

            const apiCall = axios.post(`${BACKEND_URL}/process-application`, formData);
            const delay = new Promise(resolve => setTimeout(resolve, MIN_WAIT_MS));

            const [apiResp] = await Promise.all([apiCall, delay]);

            setResult(apiResp.data);
        } catch (e) {
            console.error("Analysis failed", e);
            alert("Analysis failed. See console.");
        } finally {
            clearInterval(timerInterval);
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-indigo-500/30">
            <div className="absolute inset-0 bg-[linear-gradient(to_right,#4f4f4f2e_1px,transparent_1px),linear-gradient(to_bottom,#4f4f4f2e_1px,transparent_1px)] bg-[size:14px_24px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] pointer-events-none" />

            <div className="max-w-7xl mx-auto px-6 py-12 relative z-10">

                {/* Header */}
                <div className="text-center space-y-4 mb-16">
                    <div className="inline-flex items-center justify-center p-2 bg-slate-900/50 rounded-full mb-4 border border-slate-800 shadow-xl backdrop-blur-md">
                        <Badge variant="outline" className="bg-indigo-500/10 text-indigo-400 border-indigo-500/20 px-4 py-1 rounded-full uppercase tracking-wider text-xs font-bold">
                            <LucideSparkles className="w-3 h-3 mr-2" />
                            AI-Powered Recruitment V2.0
                        </Badge>
                    </div>
                    <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-white mb-4 drop-shadow-2xl">
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-sky-400 to-indigo-400 animate-gradient-x">
                            Smart Screen
                        </span>
                        <span className="block text-2xl md:text-3xl font-medium text-slate-400 mt-2">
                            Automated Candidate Intelligence
                        </span>
                    </h1>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">

                    {/* Left Column: Job Role */}
                    <Card className="lg:col-span-7 h-full border border-slate-800 bg-slate-900/60 backdrop-blur-xl shadow-2xl relative overflow-hidden group hover:border-slate-700 transition-all duration-300">
                        <div className="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-50" />

                        <CardHeader className="pb-4">
                            <div className="flex justify-between items-start">
                                <div>
                                    <CardTitle className="text-xl font-medium text-slate-400 flex items-center gap-2">
                                        <LucideBriefcase className="w-5 h-5 text-indigo-400" />
                                        Target Position
                                    </CardTitle>
                                </div>
                                <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={fetchNewJobRole}
                                    disabled={generatingRole}
                                    className="bg-slate-800/50 border-slate-700 text-slate-300 hover:bg-indigo-500/20 hover:text-indigo-300 hover:border-indigo-500/50 transition-all"
                                >
                                    {generatingRole ? "Generating..." : "🔄 Generate New"}
                                </Button>
                            </div>
                        </CardHeader>

                        <CardContent>
                            {!generatingRole && jobRole ? (
                                <div className="space-y-8 animate-in fade-in duration-700">

                                    {/* Title & Level */}
                                    <div>
                                        <h3 className="text-3xl md:text-4xl font-bold text-white leading-tight mb-3">
                                            {jobRole.role}
                                        </h3>
                                        <div className="flex flex-wrap gap-3">
                                            <Badge className="bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-3 py-1 text-sm font-medium hover:bg-indigo-500/30 transition-colors">
                                                {jobRole.experience_level}
                                            </Badge>
                                            <Badge variant="outline" className="text-slate-400 border-slate-700 flex items-center gap-1">
                                                <LucideGlobe className="w-3 h-3" /> Remote / Hybrid
                                            </Badge>
                                        </div>
                                    </div>

                                    <Separator className="bg-slate-800" />

                                    {/* Skills Grid */}
                                    <div>
                                        <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-widest mb-4">
                                            Required Tech Stack
                                        </h4>
                                        <div className="flex flex-wrap gap-2.5">
                                            {jobRole.skills.map((skill, i) => (
                                                <div key={i} className="px-3 py-1.5 rounded-md bg-slate-950 border border-slate-800 text-slate-300 text-sm font-medium shadow-sm hover:border-indigo-500/40 hover:text-indigo-400 transition-all cursor-default">
                                                    {skill}
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    {/* Responsibilities */}
                                    <div className="grid md:grid-cols-2 gap-8">
                                        <div>
                                            <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-widest mb-4">
                                                Key Missions
                                            </h4>
                                            <ul className="space-y-3">
                                                {jobRole.responsibilities.map((r, i) => (
                                                    <li key={i} className="flex items-start gap-3 group/item">
                                                        <LucideCheckCircle className="w-4 h-4 text-emerald-500/50 mt-1 group-hover/item:text-emerald-400 transition-colors" />
                                                        <span className="text-sm text-slate-300 leading-relaxed">{r}</span>
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>

                                        <div>
                                            <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-widest mb-4">
                                                Qualifications
                                            </h4>
                                            <ul className="space-y-3">
                                                {jobRole.qualifications.map((q, i) => (
                                                    <li key={i} className="flex items-start gap-3">
                                                        <div className="w-1.5 h-1.5 rounded-full bg-indigo-500/50 mt-2" />
                                                        <span className="text-sm text-slate-300 leading-relaxed">{q}</span>
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    </div>

                                </div>
                            ) : (
                                // Dark Skeleton Loader
                                <div className="space-y-8">
                                    <div className="space-y-3">
                                        <Skeleton className="h-12 w-3/4 bg-slate-800/50" />
                                        <Skeleton className="h-8 w-32 rounded-full bg-slate-800/50" />
                                    </div>
                                    <Separator className="bg-slate-800" />
                                    <div className="space-y-4">
                                        <Skeleton className="h-4 w-32 bg-slate-800/50" />
                                        <div className="flex flex-wrap gap-2">
                                            {[1, 2, 3, 4, 5, 6].map((_, i) => (
                                                <Skeleton key={i} className="h-8 w-24 rounded-md bg-slate-800/50" />
                                            ))}
                                        </div>
                                    </div>
                                    <div className="space-y-4">
                                        <Skeleton className="h-4 w-40 bg-slate-800/50" />
                                        <div className="space-y-3">
                                            <Skeleton className="h-4 w-full bg-slate-800/50" />
                                            <Skeleton className="h-4 w-[90%] bg-slate-800/50" />
                                            <Skeleton className="h-4 w-[95%] bg-slate-800/50" />
                                        </div>
                                    </div>
                                </div>
                            )}
                        </CardContent>
                    </Card>

                    {/* Right Column: Actions */}
                    <div className="lg:col-span-5 space-y-6 sticky top-8">

                        {/* Upload Card */}
                        <Card className="border border-slate-800 bg-slate-900 shadow-2xl overflow-hidden hover:shadow-indigo-500/10 transition-shadow duration-500">
                            <CardHeader>
                                <CardTitle className="text-white flex items-center gap-2">
                                    <LucideUpload className="text-indigo-400" />
                                    Candidate Portal
                                </CardTitle>
                                <CardDescription className="text-slate-400">
                                    Securely upload resume (PDF) for real-time AI analysis.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="border-2 border-dashed border-slate-800 rounded-xl p-8 hover:bg-slate-800/50 hover:border-indigo-500/30 transition-all text-center group">
                                    <Input
                                        id="resume"
                                        type="file"
                                        accept=".pdf"
                                        onChange={handleFileChange}
                                        className="hidden"
                                    />
                                    <Label
                                        htmlFor="resume"
                                        className="cursor-pointer flex flex-col items-center gap-3 w-full h-full"
                                    >
                                        <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center group-hover:bg-indigo-500/20 transition-colors">
                                            <LucideUpload className="w-6 h-6 text-slate-400 group-hover:text-indigo-400" />
                                        </div>
                                        <span className="text-sm font-medium text-slate-300 group-hover:text-indigo-300">
                                            {file ? file.name : "Click to Browse or Drag PDF"}
                                        </span>
                                        <span className="text-xs text-slate-500">Supported: PDF (Max 5MB)</span>
                                    </Label>
                                </div>
                            </CardContent>
                            <CardFooter>
                                <Button
                                    size="lg"
                                    className={`w-full font-bold text-lg py-6 transition-all ${loading
                                        ? "bg-slate-800 text-slate-400 cursor-not-allowed"
                                        : "bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white shadow-lg shadow-indigo-500/25"
                                        }`}
                                    onClick={handleSubmit}
                                    disabled={!file || !jobRole || loading}
                                >
                                    {loading ? (
                                        <div className="flex items-center gap-3">
                                            <div className="h-5 w-5 animate-spin rounded-full border-2 border-slate-500 border-t-white" />
                                            <span>Processing ({loadingTime}s)</span>
                                        </div>
                                    ) : "Start Alignment Analysis"}
                                </Button>
                            </CardFooter>
                        </Card>

                        {/* Results Card */}
                        {loading && (
                            <Card className="bg-slate-900 border border-slate-800 animate-in fade-in zoom-in-95 duration-500">
                                <CardContent className="py-10 flex flex-col items-center text-center">
                                    <div className="relative mb-6">
                                        <div className="absolute inset-0 bg-indigo-500 blur-xl opacity-20 animate-pulse" />
                                        <div className="h-16 w-16 rounded-full border-4 border-slate-800 border-t-indigo-500 animate-spin relative z-10" />
                                    </div>
                                    <h3 className="text-xl font-bold text-white mb-1">AI Analysis in Progress</h3>
                                    <p className="text-slate-400 text-sm">Evaluating skill matrices & experience context...</p>
                                </CardContent>
                            </Card>
                        )}

                        {!loading && result && (
                            <Card className={`border overflow-hidden shadow-2xl animate-in slide-in-from-bottom-4 duration-700 ${result.final_decision === 'Interview Scheduled'
                                ? 'bg-slate-900 border-emerald-500/30 shadow-emerald-900/20'
                                : 'bg-slate-900 border-rose-500/30 shadow-rose-900/20'
                                }`}>
                                {/* Result Header */}
                                <div className={`p-4 ${result.final_decision === 'Interview Scheduled'
                                    ? 'bg-emerald-950/30'
                                    : 'bg-rose-950/30'
                                    }`}>
                                    <div className="flex justify-between items-center">
                                        <span className="text-sm font-bold uppercase tracking-wider text-slate-400">Verdict</span>
                                        <Badge className={`${result.final_decision === 'Interview Scheduled'
                                            ? 'bg-emerald-500 text-emerald-950 hover:bg-emerald-400'
                                            : 'bg-rose-500 text-rose-950 hover:bg-rose-400'
                                            } border-0 px-3`}>
                                            {result.final_decision === 'Interview Scheduled' ? 'RECOMMENDED' : 'NOT SELECTED'}
                                        </Badge>
                                    </div>
                                </div>

                                <CardContent className="pt-6 space-y-6">
                                    <div className="flex items-center justify-between p-4 rounded-lg bg-slate-950 border border-slate-800/50">
                                        <div className="text-center">
                                            <p className="text-xs uppercase text-slate-500 font-bold tracking-widest mb-1">Experience</p>
                                            <p className="text-lg font-bold text-white">{result.experience_level}</p>
                                        </div>
                                        <div className="h-8 w-px bg-slate-800" />
                                        <div className="text-center">
                                            <p className="text-xs uppercase text-slate-500 font-bold tracking-widest mb-1">Skill Match</p>
                                            <p className={`text-lg font-bold ${result.skill_match === 'Match' ? 'text-emerald-400' : 'text-rose-400'
                                                }`}>
                                                {result.skill_match}
                                            </p>
                                        </div>
                                    </div>

                                    <div className="space-y-2">
                                        <h4 className="text-sm font-semibold text-slate-400">AI Reasoning</h4>
                                        <p className="text-slate-300 text-sm leading-relaxed">
                                            {result.final_decision === 'Interview Scheduled'
                                                ? "The candidate demonstrates strong alignment with core technical requirements and experience levels necessary for this role."
                                                : "The candidate's profile lacks critical skillsets or experience depth required for this specific seniority level."}
                                        </p>
                                    </div>
                                </CardContent>
                            </Card>
                        )}

                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;