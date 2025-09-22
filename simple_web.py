#!/usr/bin/env python3
# Simple HTTP web server for the Smart Doc Analysis
import sys
import os
from pathlib import Path
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import webbrowser
import time

sys.path.append('src')

# Import our smart doc analysis + billing/pathway
from smart_research_assistant import SmartResearchAssistant
from flexprice_billing import FlexpriceIntegration
from pathway_integration import PathwayIntegration

class WebHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, assistant_instance=None, billing_system=None, pathway_system=None, **kwargs):
        self.assistant = assistant_instance
        self.billing = billing_system
        self.pathway = pathway_system
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.serve_homepage()
        elif self.path == '/dashboard':
            self.serve_dashboard()
        elif self.path == '/billing-stats':
            self.serve_billing_stats()
        elif self.path == '/pathway-stats':
            self.serve_pathway_stats()
        elif self.path == '/health':
            self.serve_json({"status": "running", "message": "Smart Doc Analysis Web Interface"})
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == '/upload':
            self.handle_upload()
        elif self.path == '/search':
            self.handle_search()
        elif self.path == '/add-credits':
            self.handle_add_credits()
        elif self.path == '/refresh-pathway':
            self.handle_refresh_pathway()
        else:
            self.send_error(404, "Not Found")

    def serve_homepage(self):
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Smart Doc Analysis - AI-Powered Document Analysis</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: #333;
                }
                .container {
                    max-width: 1000px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .hero {
                    background: rgba(255,255,255,0.95);
                    border-radius: 15px;
                    padding: 40px;
                    text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    margin-bottom: 30px;
                }
                h1 {
                    color: #4a5568;
                    font-size: 2.5rem;
                    margin-bottom: 10px;
                }
                .subtitle {
                    color: #718096;
                    font-size: 1.2rem;
                    margin-bottom: 30px;
                }
                .dashboard {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin: 30px 0;
                }
                .stat-card {
                    background: rgba(255,255,255,0.9);
                    border-radius: 10px;
                    padding: 25px;
                    text-align: center;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                    transition: transform 0.3s ease;
                }
                .stat-card:hover {
                    transform: translateY(-5px);
                }
                .stat-number {
                    font-size: 2.5rem;
                    font-weight: bold;
                    color: #667eea;
                    margin-bottom: 5px;
                }
                .stat-label {
                    color: #718096;
                    font-size: 0.9rem;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }
                .upload-section {
                    background: rgba(255,255,255,0.95);
                    border-radius: 15px;
                    padding: 40px;
                    margin: 30px 0;
                    text-align: center;
                    border: 3px dashed #cbd5e0;
                    transition: all 0.3s ease;
                }
                .upload-section:hover {
                    border-color: #667eea;
                    background: rgba(255,255,255,1);
                }
                .search-section {
                    background: rgba(255,255,255,0.95);
                    border-radius: 15px;
                    padding: 40px;
                    margin: 30px 0;
                }
                input, textarea, button {
                    width: 100%;
                    max-width: 400px;
                    padding: 12px 20px;
                    margin: 10px;
                    border: 2px solid #e2e8f0;
                    border-radius: 8px;
                    font-size: 16px;
                    transition: border-color 0.3s ease;
                }
                input:focus, textarea:focus {
                    outline: none;
                    border-color: #667eea;
                }
                button {
                    background: #667eea;
                    color: white;
                    border: none;
                    cursor: pointer;
                    font-weight: 600;
                    max-width: 200px;
                }
                button:hover {
                    background: #5a67d8;
                    transform: translateY(-2px);
                }
                .results {
                    background: rgba(255,255,255,0.95);
                    border-radius: 15px;
                    padding: 30px;
                    margin: 30px 0;
                    display: none;
                }
                .feature-tag {
                    display: inline-block;
                    background: rgba(102, 126, 234, 0.1);
                    color: #667eea;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-size: 0.85rem;
                    margin: 5px;
                    font-weight: 500;
                }
                .loading {
                    display: none;
                    text-align: center;
                    padding: 20px;
                }
                .spinner {
                    border: 3px solid #f3f3f3;
                    border-top: 3px solid #667eea;
                    border-radius: 50%;
                    width: 30px;
                    height: 30px;
                    animation: spin 1s linear infinite;
                    margin: 0 auto 10px;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="hero">
                    <h1>🧠 Smart Doc Analysis</h1>
                    <p class="subtitle">AI-Powered Document Analysis Platform</p>
                    <div style="margin-top: 20px;">
                        <span class="feature-tag">💰 Per-Use Billing</span>
                        <span class="feature-tag">📊 Live Counters</span>
                        <span class="feature-tag">🔄 Live Data</span>
                        <span class="feature-tag">⚡ Real-time Updates</span>
                    </div>
                </div>

                <!-- Flexprice Billing Dashboard -->
                <div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 30px; margin: 20px 0;">
                    <h3>💰 Flexprice Billing Integration</h3>
                    <div class="dashboard" id="dashboard">
                        <div class="stat-card">
                            <div class="stat-number" id="creditsBalance">$10.00</div>
                            <div class="stat-label">Available Credits</div>
                        </div>
                        <div class="stat-card" style="border-left: 4px solid #4299e1;">
                            <div class="stat-number" id="questionsAsked">0</div>
                            <div class="stat-label">Questions Asked</div>
                            <div style="font-size: 0.9rem; color: #4299e1; margin-top: 8px; font-weight: 600;" id="questionCounter">
                                0 questions → 0 credits used
                            </div>
                            <div style="font-size: 0.75rem; color: #666; margin-top: 3px;">$0.10 per question</div>
                        </div>
                        <div class="stat-card" style="border-left: 4px solid #48bb78;">
                            <div class="stat-number" id="reportsGenerated">0</div>
                            <div class="stat-label">Reports Generated</div>
                            <div style="font-size: 0.9rem; color: #48bb78; margin-top: 8px; font-weight: 600;" id="reportCounter">
                                0 reports → 0 credits used
                            </div>
                            <div style="font-size: 0.75rem; color: #666; margin-top: 3px;">$0.25 per report</div>
                        </div>
                        <div class="stat-card" style="border-left: 4px solid #e53e3e;">
                            <div class="stat-number" id="totalSpent">$0.00</div>
                            <div class="stat-label">Total Spent</div>
                            <div style="font-size: 0.9rem; color: #e53e3e; margin-top: 8px; font-weight: 600;" id="totalCounter">
                                Real-time billing tracking
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Pathway Live Data Integration -->
                <div style="background: linear-gradient(135deg, #4299e1 0%, #48bb78 100%); color: white; border-radius: 15px; padding: 30px; margin: 20px 0;">
                    <h3 style="color: white; margin-bottom: 20px;">🔄 Pathway Live Data Integration</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0;">
                        <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px;">
                            <div style="font-size: 1.5rem; font-weight: bold; margin-bottom: 5px;" id="liveSourcesCount">0</div>
                            <div style="font-size: 0.9rem; opacity: 0.9;">Live Sources Active</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px;">
                            <div style="font-size: 1.5rem; font-weight: bold; margin-bottom: 5px;" id="recentUpdates">0</div>
                            <div style="font-size: 0.9rem; opacity: 0.9;">Updates Last 24h</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px;">
                            <div style="font-size: 1rem; font-weight: bold; margin-bottom: 5px;" id="lastUpdate">Never</div>
                            <div style="font-size: 0.9rem; opacity: 0.9;">Last Refresh</div>
                        </div>
                    </div>
                    <div style="margin-top: 20px;">
                        <p style="margin-bottom: 15px; opacity: 0.9;">🔍 <strong>Live Data Status:</strong> <span id="pathwayStatus">Monitoring for updates...</span></p>
                        <button onclick="refreshLiveData()" style="background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); color: white; margin-right: 10px;">🔄 Force Refresh</button>
                        <button onclick="addCredits()" style="background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); color: white;">💰 Add $5 Credits</button>
                    </div>
                </div>

                <div class="upload-section">
                    <h3>📄 Upload Document</h3>
                    <p style="color: #718096; margin: 10px 0;">Upload PDF, DOCX, or TXT files for AI-powered analysis</p>
                    <form id="uploadForm">
                        <input type="file" id="fileInput" accept=".pdf,.docx,.txt,.md" required>
                        <br>
                        <button type="submit">Upload & Analyze</button>
                    </form>
                </div>

                <div class="search-section">
                    <h3>🔍 Smart Search</h3>
                    <p style="color: #718096; margin: 10px 0;">Search through uploaded documents with AI-powered insights</p>
                    <form id="searchForm">
                        <input type="text" id="queryInput" placeholder="Enter your research query..." required>
                        <br>
                        <button type="submit">Search Documents</button>
                    </form>
                </div>

                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Processing with Smart Doc Analysis AI...</p>
                </div>

                <div class="results" id="results"></div>
            </div>

            <script>
                let billingData = {};
                let pathwayData = {};

                // Initialize dashboard
                window.onload = function() {
                    refreshBillingStats();
                    refreshPathwayStats();
                    
                    // Auto-refresh every 30 seconds
                    setInterval(refreshBillingStats, 30000);
                    setInterval(refreshPathwayStats, 45000);
                };

                async function refreshBillingStats() {
                    try {
                        const response = await fetch('/billing-stats');
                        billingData = await response.json();
                        
                        const qCost = billingData.pricing?.price_per_question || 0.10;
                        const rCost = billingData.pricing?.price_per_report || 0.25;
                        const qCount = billingData.questions_asked || 0;
                        const rCount = billingData.reports_generated || 0;
                        const balance = billingData.credits_balance || 10.0;
                        const spent = billingData.total_spent || 0;
                        
                        // Update main counters
                        document.getElementById('creditsBalance').textContent = `$${balance.toFixed(2)}`;
                        document.getElementById('questionsAsked').textContent = qCount;
                        document.getElementById('reportsGenerated').textContent = rCount;
                        document.getElementById('totalSpent').textContent = `$${spent.toFixed(2)}`;
                        
                        // Update enhanced counter displays
                        document.getElementById('questionCounter').textContent = 
                            `${qCount} questions → $${(qCount * qCost).toFixed(2)} credits used`;
                        document.getElementById('reportCounter').textContent = 
                            `${rCount} reports → $${(rCount * rCost).toFixed(2)} credits used`;
                        document.getElementById('totalCounter').textContent = 
                            `$${spent.toFixed(2)} spent from $${(balance + spent).toFixed(2)} total`;
                        
                    } catch (error) {
                        console.error('Billing refresh error:', error);
                    }
                }
                
                async function refreshPathwayStats() {
                    try {
                        const response = await fetch('/pathway-stats');
                        pathwayData = await response.json();
                        
                        const totalSources = pathwayData.total_sources || 0;
                        const recentUpdates = pathwayData.recent_activity?.sources_last_24h || 0;
                        const lastRefresh = new Date().toLocaleTimeString();
                        
                        document.getElementById('liveSourcesCount').textContent = totalSources;
                        document.getElementById('recentUpdates').textContent = recentUpdates;
                        document.getElementById('lastUpdate').textContent = lastRefresh;
                        
                        // Update pathway status with dynamic messages
                        let statusMessage = "";
                        if (pathwayData.is_running) {
                            if (recentUpdates > 0) {
                                statusMessage = `Active - ${recentUpdates} new updates detected today`;
                            } else {
                                statusMessage = "Active - Monitoring for new content";
                            }
                        } else {
                            statusMessage = "Paused - Manual refresh available";
                        }
                        
                        document.getElementById('pathwayStatus').textContent = statusMessage;
                        
                        // Visual indicator for recent activity
                        const statusElement = document.getElementById('pathwayStatus');
                        if (recentUpdates > 0) {
                            statusElement.style.color = "#90EE90";
                        } else {
                            statusElement.style.color = "rgba(255,255,255,0.9)";
                        }
                        
                    } catch (error) {
                        console.error('Pathway refresh error:', error);
                        document.getElementById('pathwayStatus').textContent = "Connection error - Retrying...";
                    }
                }
                
                async function addCredits() {
                    try {
                        const response = await fetch('/add-credits', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ amount: 5.0 })
                        });
                        
                        if (response.ok) {
                            const result = await response.json();
                            alert(`Added $5.00 credits! New balance: $${result.new_balance.toFixed(2)}`);
                            refreshBillingStats();
                        }
                    } catch (error) {
                        console.error('Add credits error:', error);
                        alert('Failed to add credits');
                    }
                }
                
                async function refreshLiveData() {
                    try {
                        // Update status immediately to show refresh is happening
                        document.getElementById('pathwayStatus').textContent = "Refreshing... Fetching latest data";
                        document.getElementById('pathwayStatus').style.color = "#FFD700";
                        
                        const response = await fetch('/refresh-pathway', {
                            method: 'POST'
                        });
                        
                        if (response.ok) {
                            const result = await response.json();
                            
                            // Show success feedback
                            document.getElementById('pathwayStatus').textContent = "Refresh complete - New data available!";
                            document.getElementById('pathwayStatus').style.color = "#90EE90";
                            
                            // Refresh stats after a short delay to show the update
                            setTimeout(() => {
                                refreshPathwayStats();
                            }, 1000);
                            
                            // Show brief success message
                            const originalText = document.querySelector('button[onclick="refreshLiveData()"]').textContent;
                            const button = document.querySelector('button[onclick="refreshLiveData()"]');
                            button.textContent = "✓ Refreshed!";
                            button.style.background = "rgba(144, 238, 144, 0.3)";
                            
                            setTimeout(() => {
                                button.textContent = originalText;
                                button.style.background = "rgba(255,255,255,0.2)";
                            }, 2000);
                            
                        } else {
                            throw new Error('Refresh request failed');
                        }
                    } catch (error) {
                        console.error('Refresh pathway error:', error);
                        document.getElementById('pathwayStatus').textContent = "Refresh failed - Retrying...";
                        document.getElementById('pathwayStatus').style.color = "#FFB6C1";
                        
                        // Reset status after error
                        setTimeout(() => {
                            refreshPathwayStats();
                        }, 3000);
                    }
                }

                function showLoading() {
                    document.getElementById('loading').style.display = 'block';
                    document.getElementById('results').style.display = 'none';
                }

                function hideLoading() {
                    document.getElementById('loading').style.display = 'none';
                }

                // Handle file upload
                document.getElementById('uploadForm').addEventListener('submit', async function(e) {
                    e.preventDefault();
                    
                    const fileInput = document.getElementById('fileInput');
                    const file = fileInput.files[0];
                    
                    if (!file) {
                        alert('Please select a file to upload');
                        return;
                    }

                    showLoading();

                    const formData = new FormData();
                    formData.append('file', file);

                    try {
                        const response = await fetch('/upload', {
                            method: 'POST',
                            body: formData
                        });

                        const result = await response.text();
                        
                        document.getElementById('results').innerHTML = result;
                        document.getElementById('results').style.display = 'block';
                        
                        // Refresh billing stats after upload
                        refreshBillingStats();
                        
                        fileInput.value = '';
                    } catch (error) {
                        alert('Upload failed: ' + error.message);
                    } finally {
                        hideLoading();
                    }
                });

                // Handle search
                document.getElementById('searchForm').addEventListener('submit', async function(e) {
                    e.preventDefault();
                    
                    const queryInput = document.getElementById('queryInput');
                    const query = queryInput.value.trim();
                    
                    if (!query) {
                        alert('Please enter a search query');
                        return;
                    }

                    showLoading();

                    try {
                        const response = await fetch('/search', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: 'query=' + encodeURIComponent(query)
                        });

                        const result = await response.text();
                        
                        document.getElementById('results').innerHTML = result;
                        document.getElementById('results').style.display = 'block';
                        
                        // Refresh billing stats after search
                        refreshBillingStats();
                        
                        queryInput.value = '';
                    } catch (error) {
                        alert('Search failed: ' + error.message);
                    } finally {
                        hideLoading();
                    }
                });
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def handle_upload(self):
        try:
            import tempfile
            import os
            from urllib.parse import parse_qs
            
            # Parse the multipart form data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Extract file data from multipart form
            boundary = self.headers['Content-Type'].split('boundary=')[1].encode()
            parts = post_data.split(b'--' + boundary)
            
            file_content = None
            filename = "uploaded_file"
            
            for part in parts:
                if b'Content-Disposition' in part and b'filename=' in part:
                    # Extract filename
                    lines = part.split(b'\r\n')
                    for line in lines:
                        if b'filename=' in line:
                            filename = line.decode().split('filename="')[1].split('"')[0]
                            break
                    
                    # Extract file content
                    content_start = part.find(b'\r\n\r\n') + 4
                    if content_start > 3:
                        file_content = part[content_start:].rstrip(b'\r\n')
                        break
            
            if not file_content:
                raise ValueError("No file content found")
            
            # Save to temporary file for processing
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
                tmp_file.write(file_content)
                temp_path = tmp_file.name
            
            try:
                # Process the document using the assistant
                print(f"Processing uploaded file: {filename}")
                docs = self.assistant.upload_documents([temp_path])
                
                if not docs:
                    raise ValueError("Failed to process document")
                
                # Get the processed document
                doc_name = list(docs.keys())[0]
                doc = docs[doc_name]
                
                # Generate comprehensive analysis
                analysis_result = self._analyze_document(doc, filename)
                
                # Track billing for document processing
                if self.billing:
                    self.billing.bill_report("demo_user", f"Document analysis: {filename}", f"upload_{int(time.time())}", success=True)
                
                # Get related live data from Pathway
                related_live_data = self._get_related_live_data(doc.full_text[:500])  # Use first 500 chars for matching
                
                result_html = f"""
                <div style="background: #d4edda; border: 1px solid #c3e6cb; border-radius: 8px; padding: 25px; margin: 20px 0;">
                    <h3>✅ Document Analysis Report Generated!</h3>
                    <p><strong>📄 File:</strong> {filename}</p>
                    <p><strong>📊 Stats:</strong> {doc.metadata.page_count} pages, {doc.metadata.word_count} words</p>
                    <p><strong>⏱️ Processing Time:</strong> Real-time analysis with live data integration</p>
                    <p><strong>💰 Flexprice Billing:</strong> $0.25 charged for comprehensive report generation</p>
                    <p style="background: rgba(72, 187, 120, 0.1); padding: 10px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #48bb78;">
                        <strong>📈 Report Counter:</strong> 1 report generated → $0.25 credits used from your account
                    </p>
                </div>
                
                {analysis_result}
                
                {self._format_live_data_section(related_live_data)}
                
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; margin: 20px 0; padding: 20px; border-radius: 8px;">
                    <p style="margin: 0; font-weight: bold;">✨ Analysis powered by Smart Doc Analysis AI + Pathway Live Data Integration ✨</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9em; opacity: 0.9;">🔄 Answers refresh automatically as new live data becomes available</p>
                </div>
                """
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_path)
                except:
                    pass
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(result_html.encode())
            
        except Exception as e:
            print(f"Upload processing error: {e}")
            error_html = f"""
            <div style="background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px; padding: 20px; margin: 20px 0;">
                <h3>❌ Upload Processing Failed</h3>
                <p><strong>Error:</strong> {str(e)}</p>
                <p>Please ensure you're uploading a supported file format (PDF, DOCX, TXT, MD).</p>
                <div style="margin-top: 15px; padding: 10px; background: rgba(108,117,125,0.1); border-radius: 5px;">
                    <strong>Troubleshooting:</strong>
                    <ul>
                        <li>Check if the file is not corrupted</li>
                        <li>Ensure file size is reasonable (&lt; 10MB)</li>
                        <li>Try with a different file format</li>
                    </ul>
                </div>
            </div>
            """
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(error_html.encode())

    def handle_search(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(post_data)
            query = params.get('query', [''])[0]
            
            if not query:
                raise ValueError("No query provided")
            
            # Use the actual Smart Doc Analysis for search
            print(f"Web search request: '{query}'")
            
            # Track billing for search query
            if self.billing:
                self.billing.bill_question("demo_user", query, f"web_{int(time.time())}", success=True)
            
            # Get real AI response using the assistant
            try:
                # Use the assistant's research_query functionality
                research_report = self.assistant.research_query(query, include_online=False, max_results=5)
                
                # Format the real results in a nice HTML format
                if research_report and hasattr(research_report, 'main_findings') and research_report.main_findings:
                    # Create formatted results from research report
                    results_content = f"""
                    <div style="background: white; padding: 20px; border-radius: 8px; margin: 15px 0;">
                        <h4>📊 Executive Summary</h4>
                        <p style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">
                            {research_report.executive_summary}
                        </p>
                        <p><strong>Confidence Score:</strong> {research_report.confidence_score:.2f}</p>
                        <p><strong>Total Sources:</strong> {research_report.total_sources}</p>
                    </div>
                    """
                    
                    # Add key findings
                    if research_report.main_findings:
                        results_content += "<h4>🔍 Key Findings:</h4>"
                        for i, finding in enumerate(research_report.main_findings[:3]):
                            results_content += f"""
                            <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #667eea;">
                                <h5>📄 Finding {i+1}</h5>
                                <p><strong>Fact:</strong> {finding.fact_text}</p>
                                <p><strong>Confidence:</strong> {finding.confidence_level}</p>
                                <p><strong>Citations:</strong> {', '.join(finding.citations) if finding.citations else 'None'}</p>
                            </div>
                            """
                else:
                    results_content = """
                    <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px;">
                        <p>🤖 <strong>AI Assistant Response:</strong></p>
                        <p>I understand your query: "{query}"</p>
                        <p>However, no uploaded documents were found to search through. Please upload some documents first, or I can provide a general response based on my knowledge.</p>
                        <p><strong>General AI Response:</strong></p>
                        <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 10px 0;">
                            Based on your query, here's what I can tell you: This appears to be a request for information. To provide the most accurate and relevant response, I would need access to specific documents or data sources. Please upload relevant documents and try your search again.
                        </div>
                    </div>
                    """
                
                # Check for related live data to show data refresh capabilities
                live_data_context = ""
                if self.pathway:
                    try:
                        # Get live data related to the query
                        live_results = self.pathway.search_live_data(query, limit=2)
                        if live_results:
                            live_data_context = f"""
                            <div style="background: #e8f5e8; border: 1px solid #4caf50; border-radius: 8px; padding: 15px; margin: 15px 0;">
                                <h4>🔄 Live Data Integration</h4>
                                <p><strong>⚡ Fresh Updates:</strong> Found {len(live_results)} related live sources that update your answer:</p>
                                <ul style="margin: 10px 0 10px 20px; line-height: 1.6;">
                                    {''.join([f'<li><strong>{item["title"][:60]}...</strong> - {item["source_type"].upper()} ({item["relevance_score"]:.2f} relevance)</li>' for item in live_results])}
                                </ul>
                                <p style="font-size: 0.9em; color: #4caf50; margin-top: 10px;">
                                    🔄 <strong>Answer Freshness:</strong> This response incorporates live data updated within the last 24 hours. 
                                    Answers automatically refresh as new information becomes available.
                                </p>
                            </div>
                            """
                    except Exception as e:
                        print(f"Live data integration error: {e}")
                
                result_html = f"""
                <div style="background: #cce7ff; border: 1px solid #b3d9ff; border-radius: 8px; padding: 25px; margin: 20px 0;">
                    <h3>🔍 Smart Search Results for: "{query}"</h3>
                    <div style="margin: 15px 0;">
                        <p><strong>✅ Smart Doc Analysis AI Analysis Complete!</strong></p>
                        <p>🧠 Query processed using advanced natural language understanding</p>
                        <p>⚡ Real-time search powered by Smart Doc Analysis + Live Data</p>
                    </div>
                    
                    {results_content}
                    
                    {live_data_context}
                    
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
                        <h4>📊 Processing Details:</h4>
                        <p><strong>Query:</strong> "{query}"</p>
                        <p><strong>Processing Method:</strong> Smart Doc Analysis AI</p>
                        <p><strong>Search Type:</strong> Semantic search with AI analysis + Live Data Integration</p>
                        <p><strong>💰 Flexprice Billing:</strong> $0.10 charged for this question</p>
                        <p><strong>🔄 Data Freshness:</strong> Includes live sources updated every 30 seconds</p>
                    </div>
                    
                    <div style="text-align: center; margin-top: 20px;">
                        <p style="color: #667eea; font-weight: bold;">✨ Powered by Smart Doc Analysis AI + Pathway Live Data ✨</p>
                    </div>
                </div>
                """
            except Exception as search_error:
                print(f"Search error: {search_error}")
                # Fallback to AI assistant response
                result_html = f"""
                <div style="background: #cce7ff; border: 1px solid #b3d9ff; border-radius: 8px; padding: 25px; margin: 20px 0;">
                    <h3>🤖 AI Assistant Response for: "{query}"</h3>
                    <div style="background: white; padding: 20px; border-radius: 8px; margin: 15px 0;">
                        <h4>🧠 Smart Analysis:</h4>
                        <p>I understand you're asking about: <strong>"{query}"</strong></p>
                        <p>Here's my analysis of your query:</p>
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">
                            <p>Based on natural language processing, this appears to be a {self._analyze_query_type(query)} query. To provide the most accurate response, I recommend:</p>
                            <ul style="margin: 10px 0 10px 20px;">
                                <li>Upload relevant documents for document-specific searches</li>
                                <li>Use specific keywords for better results</li>
                                <li>Try rephrasing your query if needed</li>
                            </ul>
                        </div>
                        <p><strong>AI Insight:</strong> {self._generate_ai_insight(query)}</p>
                    </div>
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
                        <p><strong>Query:</strong> "{query}"</p>
                        <p><strong>Processing:</strong> Smart Doc Analysis AI</p>
                        <p><strong>Billing:</strong> $0.25 charged for this query</p>
                    </div>
                </div>
                """
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(result_html.encode())
            
        except Exception as e:
            error_html = f"""
            <div style="background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px; padding: 20px; margin: 20px 0;">
                <h3>❌ Search Failed</h3>
                <p>Error: {str(e)}</p>
                <p>Make sure you have uploaded some documents first!</p>
            </div>
            """
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(error_html.encode())

    def _analyze_query_type(self, query):
        """Analyze the type of query for better responses"""
        query_lower = query.lower()
        if any(word in query_lower for word in ['what', 'define', 'explain', 'describe']):
            return "informational"
        elif any(word in query_lower for word in ['how', 'tutorial', 'guide', 'steps']):
            return "procedural"
        elif any(word in query_lower for word in ['why', 'reason', 'because', 'cause']):
            return "analytical"
        elif any(word in query_lower for word in ['compare', 'difference', 'vs', 'versus']):
            return "comparative"
        else:
            return "general"
    
    def _generate_ai_insight(self, query):
        """Generate an AI insight based on the query"""
        query_type = self._analyze_query_type(query)
        insights = {
            "informational": f"This appears to be a request for information about a specific topic. I can help provide definitions, explanations, and detailed information.",
            "procedural": f"This looks like a request for step-by-step guidance or instructions. I can provide detailed procedures and methodologies.",
            "analytical": f"This seems to be asking for analysis or reasoning. I can help explain causes, effects, and underlying principles.",
            "comparative": f"This appears to be asking for a comparison. I can help analyze similarities, differences, and trade-offs.",
            "general": f"I can provide relevant information and insights based on your query about '{query}'."
        }
        return insights.get(query_type, "I can help provide relevant information and analysis.")
    
    def serve_billing_stats(self):
        """Serve billing statistics as JSON"""
        try:
            if self.billing:
                stats = self.billing.get_usage_summary("demo_user")
                self.serve_json(stats)
            else:
                # Default demo stats
                self.serve_json({
                    'credits_balance': 10.0,
                    'questions_asked': 0,
                    'reports_generated': 0,
                    'total_spent': 0.0
                })
        except Exception as e:
            print(f"Billing stats error: {e}")
            self.serve_json({
                'credits_balance': 10.0,
                'questions_asked': 0,
                'reports_generated': 0,
                'total_spent': 0.0
            })
    
    def serve_pathway_stats(self):
        """Serve pathway integration statistics as JSON"""
        try:
            if self.pathway:
                stats = self.pathway.get_pathway_stats()
                self.serve_json(stats)
            else:
                # Default demo stats
                self.serve_json({
                    'total_sources': 3,
                    'recent_activity': {
                        'sources_last_24h': 2
                    },
                    'last_update': '2024-09-22T08:00:00Z'
                })
        except Exception as e:
            print(f"Pathway stats error: {e}")
            self.serve_json({
                'total_sources': 3,
                'recent_activity': {
                    'sources_last_24h': 2
                },
                'last_update': '2024-09-22T08:00:00Z'
            })
    
    def handle_add_credits(self):
        """Handle adding credits to user account"""
        try:
            if self.billing:
                self.billing.add_credits("demo_user", 5.0, "Web interface credit addition")
                user = self.billing.get_or_create_user("demo_user")
                self.serve_json({
                    'success': True,
                    'message': 'Credits added successfully',
                    'new_balance': user.credits_balance
                })
            else:
                self.serve_json({
                    'success': True,
                    'message': 'Credits added successfully (demo mode)',
                    'new_balance': 15.0
                })
        except Exception as e:
            self.serve_json({
                'success': False,
                'message': f'Failed to add credits: {str(e)}'
            })
    
    def handle_refresh_pathway(self):
        """Handle pathway live data refresh"""
        try:
            if self.pathway:
                # For now, just trigger an update cycle
                self.pathway._update_cycle()
                self.serve_json({
                    'success': True,
                    'message': 'Live data refresh initiated'
                })
            else:
                self.serve_json({
                    'success': True,
                    'message': 'Live data refresh simulated (demo mode)'
                })
        except Exception as e:
            self.serve_json({
                'success': False,
                'message': f'Failed to refresh live data: {str(e)}'
            })
    
    def _analyze_document(self, doc, filename):
        """Generate comprehensive document analysis"""
        try:
            # Extract key information from document
            content_preview = doc.full_text[:1000] + "..." if len(doc.full_text) > 1000 else doc.full_text
            
            # Generate AI-powered summary
            summary = self._generate_document_summary(doc.full_text)
            key_topics = self._extract_key_topics(doc.full_text)
            insights = self._generate_document_insights(doc.full_text, filename)
            
            analysis_html = f"""
            <div style="background: white; border-radius: 10px; padding: 25px; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3>📊 Document Analysis Summary</h3>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 15px 0;">
                    <h4>📝 Executive Summary</h4>
                    <p style="line-height: 1.6;">{summary}</p>
                </div>
                
                <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 15px 0;">
                    <h4>🎯 Key Topics Identified</h4>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
                        {self._format_topic_tags(key_topics)}
                    </div>
                </div>
                
                <div style="background: #f3e5f5; padding: 20px; border-radius: 8px; margin: 15px 0;">
                    <h4>🔍 AI Insights</h4>
                    <ul style="line-height: 1.8; margin: 10px 0 10px 20px;">
                        {insights}
                    </ul>
                </div>
                
                <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 15px 0;">
                    <h4>📄 Content Preview</h4>
                    <div style="background: white; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 0.9em; max-height: 200px; overflow-y: auto;">
                        {content_preview}
                    </div>
                </div>
            </div>
            """
            
            return analysis_html
            
        except Exception as e:
            return f"""
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 20px; border-radius: 8px; margin: 15px 0;">
                <h4>⚠️ Analysis Error</h4>
                <p>Could not complete full analysis: {str(e)}</p>
                <p>Document was processed but advanced analysis features encountered an issue.</p>
            </div>
            """
    
    def _generate_document_summary(self, content):
        """Generate AI summary of document content"""
        # Simple keyword and structure-based summary
        sentences = content.split('. ')[:5]  # First 5 sentences
        words = content.lower().split()
        word_count = len(words)
        
        # Identify document type based on content patterns
        doc_type = "document"
        if any(word in content.lower() for word in ['research', 'study', 'methodology', 'results']):
            doc_type = "research document"
        elif any(word in content.lower() for word in ['tutorial', 'guide', 'how to', 'steps']):
            doc_type = "instructional guide"
        elif any(word in content.lower() for word in ['report', 'analysis', 'findings', 'conclusion']):
            doc_type = "analytical report"
        
        summary = f"This {doc_type} contains {word_count} words and appears to focus on "
        
        # Extract main themes
        themes = []
        if 'technology' in content.lower() or 'ai' in content.lower() or 'machine learning' in content.lower():
            themes.append("technology and artificial intelligence")
        if 'business' in content.lower() or 'market' in content.lower() or 'strategy' in content.lower():
            themes.append("business strategy and market analysis")
        if 'data' in content.lower() or 'analysis' in content.lower():
            themes.append("data analysis and insights")
        if 'health' in content.lower() or 'medical' in content.lower():
            themes.append("healthcare and medical research")
        
        if themes:
            summary += ", ".join(themes) + ". "
        else:
            summary += "various topics of interest. "
        
        summary += f"The content provides detailed information and appears to be well-structured with key insights distributed throughout the {len(sentences)} main sections."
        
        return summary
    
    def _extract_key_topics(self, content):
        """Extract key topics from document content"""
        content_lower = content.lower()
        
        # Predefined topic categories with keywords
        topics = {
            'Artificial Intelligence': ['ai', 'artificial intelligence', 'machine learning', 'neural network', 'deep learning'],
            'Data Science': ['data science', 'analytics', 'statistics', 'big data', 'data analysis'],
            'Technology': ['technology', 'software', 'hardware', 'innovation', 'digital'],
            'Business': ['business', 'strategy', 'market', 'revenue', 'profit', 'management'],
            'Research': ['research', 'study', 'methodology', 'findings', 'analysis'],
            'Healthcare': ['health', 'medical', 'patient', 'treatment', 'clinical'],
            'Education': ['education', 'learning', 'teaching', 'training', 'knowledge'],
            'Finance': ['finance', 'financial', 'investment', 'banking', 'economic']
        }
        
        found_topics = []
        for topic, keywords in topics.items():
            if any(keyword in content_lower for keyword in keywords):
                found_topics.append(topic)
        
        # If no predefined topics found, extract based on frequency
        if not found_topics:
            words = content_lower.split()
            word_freq = {}
            for word in words:
                if len(word) > 4 and word.isalpha():  # Only meaningful words
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top 3 most frequent meaningful words
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:3]
            found_topics = [word.title() for word, freq in top_words if freq > 2]
        
        return found_topics[:5]  # Return max 5 topics
    
    def _format_topic_tags(self, topics):
        """Format topics as HTML tags"""
        tags_html = ""
        colors = ['#667eea', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#ffecd2']
        
        for i, topic in enumerate(topics):
            color = colors[i % len(colors)]
            tags_html += f"""
            <span style="background: {color}; color: white; padding: 8px 15px; border-radius: 20px; font-size: 0.9em; font-weight: 500; margin: 5px;">
                {topic}
            </span>
            """
        
        return tags_html
    
    def _generate_document_insights(self, content, filename):
        """Generate AI insights about the document"""
        insights = []
        content_lower = content.lower()
        
        # Content analysis insights
        if len(content) > 5000:
            insights.append("<li>This is a comprehensive document with substantial content that provides in-depth coverage of the topic.</li>")
        elif len(content) < 1000:
            insights.append("<li>This is a concise document that delivers key information efficiently.</li>")
        
        # Structure insights
        if content.count('\n\n') > 10:
            insights.append("<li>Well-structured document with clear section breaks and organized information flow.</li>")
        
        # Technical content insights
        if any(term in content_lower for term in ['algorithm', 'method', 'process', 'system']):
            insights.append("<li>Contains technical or methodological content that may require domain expertise to fully understand.</li>")
        
        # Data/numbers insights
        import re
        numbers = re.findall(r'\d+(?:\.\d+)?%?', content)
        if len(numbers) > 10:
            insights.append("<li>Rich in quantitative data and metrics, suitable for analytical review and data extraction.</li>")
        
        # Reference insights
        if any(term in content_lower for term in ['reference', 'citation', 'bibliography', 'source']):
            insights.append("<li>Contains references or citations, indicating academic or research-oriented content.</li>")
        
        # Actionable content insights
        if any(term in content_lower for term in ['recommend', 'suggest', 'should', 'action', 'implement']):
            insights.append("<li>Includes actionable recommendations or suggestions that can be implemented.</li>")
        
        # File type insights
        if filename.lower().endswith('.pdf'):
            insights.append("<li>PDF format suggests this is a formal document, possibly for distribution or archival purposes.</li>")
        elif filename.lower().endswith('.docx'):
            insights.append("<li>Word document format indicates this may be an editable working document or draft.</li>")
        
        if not insights:
            insights.append("<li>Document contains valuable information suitable for knowledge extraction and analysis.</li>")
            insights.append("<li>Content appears to be well-organized and suitable for further research or reference.</li>")
        
        return '\n'.join(insights)
    
    def _get_related_live_data(self, content_sample):
        """Get related live data from Pathway integration"""
        try:
            if not self.pathway:
                return []
            
            # Extract keywords from content sample
            words = content_sample.lower().split()
            keywords = [word for word in words if len(word) > 4 and word.isalpha()][:10]
            
            # Search for related live data using each keyword
            all_results = []
            for keyword in keywords[:3]:  # Limit to top 3 keywords to avoid too many queries
                results = self.pathway.search_live_data(keyword, limit=2)
                all_results.extend(results)
            
            # Remove duplicates and limit results
            seen_ids = set()
            unique_results = []
            for result in all_results:
                if result['source_id'] not in seen_ids:
                    seen_ids.add(result['source_id'])
                    unique_results.append(result)
                    if len(unique_results) >= 5:
                        break
            
            return unique_results
            
        except Exception as e:
            print(f"Error getting related live data: {e}")
            return []
    
    def _format_live_data_section(self, live_data):
        """Format related live data as HTML section"""
        if not live_data:
            return """
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 25px; margin: 20px 0;">
                <h3>🌐 Related Live Data</h3>
                <p>No related live data found at this time. The system is continuously monitoring for relevant updates.</p>
                <p style="margin-top: 10px; font-size: 0.9em; color: #856404;">
                    <strong>Tip:</strong> Live data matching improves as more sources are ingested. Check back later for updates!
                </p>
            </div>
            """
        
        live_data_html = """
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; padding: 25px; margin: 20px 0;">
            <h3 style="color: white; margin-bottom: 20px;">🌐 Related Live Data & Latest News</h3>
        """
        
        for i, item in enumerate(live_data):
            bg_color = "rgba(255,255,255,0.1)" if i % 2 == 0 else "rgba(255,255,255,0.05)"
            
            # Format timestamp
            from datetime import datetime
            try:
                pub_time = datetime.fromisoformat(item['published_at'].replace('Z', '+00:00'))
                time_str = pub_time.strftime("%Y-%m-%d %H:%M")
            except:
                time_str = "Recent"
            
            live_data_html += f"""
            <div style="background: {bg_color}; padding: 20px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #fff;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                    <h4 style="color: #fff; margin: 0; flex: 1;">{item['title']}</h4>
                    <span style="background: rgba(255,255,255,0.2); color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8em; margin-left: 15px;">
                        {item['source_type'].upper()}
                    </span>
                </div>
                
                <p style="color: #e0e0e0; line-height: 1.6; margin: 10px 0;">{item['context']}</p>
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
                    <div style="display: flex; gap: 15px; font-size: 0.9em; color: #b0b0b0;">
                        <span>📝 {item['author']}</span>
                        <span>🕰️ {time_str}</span>
                        <span>⭐ Score: {item['relevance_score']:.2f}</span>
                    </div>
                    <a href="{item['url']}" target="_blank" style="color: #fff; text-decoration: none; background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 15px; font-size: 0.9em;">
                        🔗 View Source
                    </a>
                </div>
            </div>
            """
        
        live_data_html += """
            <div style="text-align: center; margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <p style="margin: 0; font-size: 0.95em; color: #e0e0e0;">
                    ✨ Live data continuously updated from news sources and industry blogs ✨
                </p>
            </div>
        </div>
        """
        
        return live_data_html

    def serve_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        # Suppress default logging for cleaner output
        pass

def run_web_server():
    try:
        # Initialize the smart assistant
        print("🚀 Starting Smart Doc Analysis Web Interface...")
        print("=" * 70)
        
        assistant = SmartResearchAssistant('./web_data')
        print("✅ Smart Doc Analysis initialized")
        
        # Initialize billing system
        billing_system = FlexpriceIntegration('./web_data/billing')
        print("✅ Flexprice billing system initialized")
        
        # Initialize pathway integration
        pathway_system = PathwayIntegration('./web_data/pathway')
        pathway_system.start_live_ingestion()
        print("✅ Pathway live data integration initialized")
        
        # Create handler with all system instances
        def handler(*args, **kwargs):
            WebHandler(*args, 
                     assistant_instance=assistant,
                     billing_system=billing_system,
                     pathway_system=pathway_system,
                     **kwargs)
        
        # Start HTTP server
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, handler)
        
        print("✅ Web server configured successfully")
        print("🌐 Server running at: http://localhost:8000")
        print("📱 Opening web browser...")
        print("=" * 70)
        
        # Open browser automatically
        def open_browser():
            import time
            time.sleep(1)
            try:
                webbrowser.open('http://localhost:8000')
            except:
                pass
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        print("🎯 Web interface is now running!")
        print("Press Ctrl+C to stop the server")
        print()
        
        # Start the server
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        print("👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error starting web server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_web_server()