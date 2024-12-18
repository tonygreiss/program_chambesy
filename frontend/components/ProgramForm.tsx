'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

interface ProgramFormData {
  month: string
  year: number
  frenchVerse: string
  arabicVerse: string
}

export default function ProgramForm() {
  const [isLoading, setIsLoading] = useState(false)
  const [selectedMonth, setSelectedMonth] = useState<string>('')
  const { register, handleSubmit, formState: { errors } } = useForm<ProgramFormData>()

  const months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
  ]

  const currentYear = new Date().getFullYear()

  const onSubmit = async (data: ProgramFormData) => {
    if (!selectedMonth) {
      return;
    }

    try {
      setIsLoading(true);
      
      const formData = {
        month: parseInt(selectedMonth) + 1,
        year: parseInt(data.year),
        french_verse: data.frenchVerse,
        arabic_verse: data.arabicVerse
      };

      console.log('Submitting form with data:', formData);

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/generate-program`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Server error:', errorData);
        throw new Error(errorData.error || 'Failed to generate program');
      }

      // Get the blob from the response
      const blob = await response.blob();
      
      // Create a download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `program_${formData.month}_${formData.year}.docx`;
      
      // Trigger the download
      document.body.appendChild(a);
      a.click();
      
      // Cleanup
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      console.log('Program generated and downloaded successfully');

    } catch (error) {
      console.error('Error generating program:', error);
      // You might want to add some UI feedback here
      alert(`Error generating program: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-8 max-w-2xl mx-auto p-8 bg-white rounded-lg shadow-md border border-gray-200">
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-gray-900">Generate Church Program</h2>
        <p className="text-gray-600">Fill in the details below to generate a new program.</p>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="space-y-2">
          <Label htmlFor="month" className="text-gray-700 font-medium">Month</Label>
          <Select 
            onValueChange={(value) => setSelectedMonth(value)}
          >
            <SelectTrigger className="bg-white border-gray-300">
              <SelectValue placeholder="Select month" />
            </SelectTrigger>
            <SelectContent>
              {months.map((month, index) => (
                <SelectItem key={index} value={index.toString()}>
                  {month}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {!selectedMonth && (
            <p className="text-sm text-red-500">Month is required</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="year" className="text-gray-700 font-medium">Year</Label>
          <Input
            type="number"
            id="year"
            min={currentYear}
            max={currentYear + 10}
            defaultValue={currentYear}
            className="bg-white border-gray-300"
            {...register('year', { 
              required: 'Year is required',
              min: {
                value: currentYear,
                message: `Year must be ${currentYear} or later`
              },
              max: {
                value: currentYear + 10,
                message: `Year must be no later than ${currentYear + 10}`
              }
            })}
          />
          {errors.year && (
            <p className="text-sm text-red-500">{errors.year.message}</p>
          )}
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="frenchVerse" className="text-gray-700 font-medium">French Verse</Label>
        <Textarea
          id="frenchVerse"
          placeholder="Enter the verse in French"
          {...register('frenchVerse', { required: true })}
          className="min-h-[100px] bg-white border-gray-300"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="arabicVerse" className="text-gray-700 font-medium">Arabic Verse</Label>
        <Textarea
          id="arabicVerse"
          placeholder="Enter the verse in Arabic"
          {...register('arabicVerse', { required: true })}
          className="min-h-[100px] text-right bg-white border-gray-300"
          dir="rtl"
        />
      </div>

      <Button 
        type="submit" 
        className="w-full"
        disabled={isLoading}
      >
        {isLoading ? 'Generating...' : 'Generate Program'}
      </Button>
    </form>
  )
} 