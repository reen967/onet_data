import React, { useState, useEffect } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import Papa from 'papaparse';

export default function OrgMappingForm() {
  const [departments, setDepartments] = useState([]);
  const [roles, setRoles] = useState([]);
  const [currentDept, setCurrentDept] = useState('');
  const [currentRole, setCurrentRole] = useState({ name: '', dept: '', description: '', headcount: 1 });
  const [selectedRole, setSelectedRole] = useState(null);
  const [roleDetails, setRoleDetails] = useState({ tasks: [], skills: [], knowledge: [] });

  const addDepartment = () => {
    if (currentDept && !departments.includes(currentDept)) {
      setDepartments([...departments, currentDept]);
      setCurrentDept('');
    }
  };

  const addRole = () => {
    if (currentRole.name && currentRole.dept) {
      setRoles([...roles, currentRole]);
      setCurrentRole({ name: '', dept: '', description: '', headcount: 1 });
    }
  };

  const handleRoleSelect = async (roleName) => {
    setSelectedRole(roleName);

    const occupationData = await loadCSV('occupation_data.csv');
    const matched = occupationData.find(row => row.Title.toLowerCase() === roleName.toLowerCase());

    if (!matched) return;

    const socCode = matched['O*NET-SOC Code'];

    const tasks = await loadCSV('task_statements.csv');
    const skills = await loadCSV('skills.csv');
    const knowledge = await loadCSV('knowledge.csv');

    const filteredTasks = tasks.filter(row => row['O*NET-SOC Code'] === socCode).map(row => row['Task']);
    const filteredSkills = skills.filter(row => row['O*NET-SOC Code'] === socCode).map(row => row['Element Name']);
    const filteredKnowledge = knowledge.filter(row => row['O*NET-SOC Code'] === socCode).map(row => row['Element Name']);

    setRoleDetails({ tasks: filteredTasks, skills: filteredSkills, knowledge: filteredKnowledge });
  };

  const loadCSV = (filename) => {
    return new Promise((resolve, reject) => {
      Papa.parse(`/${filename}`, {
        header: true,
        download: true,
        complete: (results) => resolve(results.data),
        error: (err) => reject(err),
      });
    });
  };

  return (
    <div className="p-4 space-y-6">
      <Card>
        <CardContent className="space-y-4">
          <h2 className="text-xl font-semibold">Add Department</h2>
          <div className="flex items-center gap-2">
            <Input
              placeholder="Department name"
              value={currentDept}
              onChange={e => setCurrentDept(e.target.value)}
            />
            <Button onClick={addDepartment}>Add</Button>
          </div>
          <div className="text-sm text-muted-foreground">
            {departments.length > 0 && `Departments: ${departments.join(', ')}`}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="space-y-4">
          <h2 className="text-xl font-semibold">Add Role</h2>
          <Input
            placeholder="Role name"
            value={currentRole.name}
            onChange={e => setCurrentRole({ ...currentRole, name: e.target.value })}
          />
          <select
            className="border rounded p-2 w-full"
            value={currentRole.dept}
            onChange={e => setCurrentRole({ ...currentRole, dept: e.target.value })}
          >
            <option value="">Select department</option>
            {departments.map(dept => (
              <option key={dept} value={dept}>{dept}</option>
            ))}
          </select>
          <Textarea
            placeholder="Role description or key responsibilities"
            value={currentRole.description}
            onChange={e => setCurrentRole({ ...currentRole, description: e.target.value })}
          />
          <Input
            type="number"
            placeholder="Headcount"
            value={currentRole.headcount}
            onChange={e => setCurrentRole({ ...currentRole, headcount: parseInt(e.target.value || '1', 10) })}
          />
          <Button onClick={addRole}>Add Role</Button>

          <div className="mt-4">
            <h3 className="text-md font-semibold">Roles Added</h3>
            <ul className="text-sm text-muted-foreground">
              {roles.map((role, idx) => (
                <li key={idx} onClick={() => handleRoleSelect(role.name)} className="cursor-pointer text-blue-600 hover:underline">
                  {role.name} ({role.headcount}) – {role.dept}
                </li>
              ))}
            </ul>
          </div>
        </CardContent>
      </Card>

      {selectedRole && (
        <Card>
          <CardContent className="space-y-4">
            <h2 className="text-xl font-semibold">{selectedRole} Details</h2>
            <div>
              <h3 className="font-semibold">Tasks</h3>
              <ul className="list-disc pl-5">
                {roleDetails.tasks.map((task, idx) => (
                  <li key={idx}>{task}</li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="font-semibold">Skills</h3>
              <ul className="list-disc pl-5">
                {roleDetails.skills.map((skill, idx) => (
                  <li key={idx}>{skill}</li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="font-semibold">Knowledge</h3>
              <ul className="list-disc pl-5">
                {roleDetails.knowledge.map((knowledge, idx) => (
                  <li key={idx}>{knowledge}</li>
                ))}
              </ul>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
