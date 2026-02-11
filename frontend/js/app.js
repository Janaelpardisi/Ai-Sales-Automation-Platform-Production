// API Base URL
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Toggle Campaign Form
function toggleCampaignForm() {
    const container = document.getElementById('campaign-form-container');
    const arrow = document.getElementById('form-arrow');

    if (container.style.maxHeight === '0px' || container.style.maxHeight === '') {
        container.style.maxHeight = '500px';
        arrow.style.transform = 'rotate(180deg)';
    } else {
        container.style.maxHeight = '0px';
        arrow.style.transform = 'rotate(0deg)';
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function () {
    loadStats();
    loadCampaigns();
    loadLeads();

    // Setup form submission
    document.getElementById('campaign-form').addEventListener('submit', createCampaign);
});

// Show Toast Notification
function showToast(message, type = 'info') {
    const colors = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        info: 'bg-blue-500',
        warning: 'bg-yellow-500'
    };

    const icons = {
        success: '✅',
        error: '❌',
        info: 'ℹ️',
        warning: '⚠️'
    };

    const toast = document.createElement('div');
    toast.className = `${colors[type]} text-white px-6 py-4 rounded-lg shadow-lg flex items-center space-x-3 transform transition-all duration-300 translate-x-0`;
    toast.innerHTML = `
        <span class="text-2xl">${icons[type]}</span>
        <div>
            <div class="font-semibold">${type.charAt(0).toUpperCase() + type.slice(1)}</div>
            <div class="text-sm">${message}</div>
        </div>
    `;

    document.getElementById('toast-container').appendChild(toast);

    // Slide in
    setTimeout(() => toast.classList.add('translate-x-0'), 10);

    // Remove after 3 seconds
    setTimeout(() => {
        toast.classList.add('translate-x-full', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Load Stats
async function loadStats() {
    try {
        const [campaignsRes, leadsRes] = await Promise.all([
            fetch(`${API_BASE_URL}/campaigns`),
            fetch(`${API_BASE_URL}/leads`)
        ]);

        const campaigns = await campaignsRes.json();
        const leads = await leadsRes.json();

        // Calculate stats
        let totalEmailsSent = 0;
        let totalEmailsReplied = 0;

        campaigns.items?.forEach(c => {
            totalEmailsSent += c.emails_sent || 0;
            totalEmailsReplied += c.emails_replied || 0;
        });

        const replyRate = totalEmailsSent > 0
            ? ((totalEmailsReplied / totalEmailsSent) * 100).toFixed(1)
            : 0;

        // Update UI
        document.getElementById('total-campaigns').textContent = campaigns.total || 0;
        document.getElementById('total-leads').textContent = leads.total || 0;
        document.getElementById('emails-sent').textContent = totalEmailsSent;
        document.getElementById('reply-rate').textContent = `${replyRate}%`;

    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Create Campaign
async function createCampaign(e) {
    e.preventDefault();

    const btn = document.getElementById('create-btn-text');
    const loader = document.getElementById('create-loader');

    // Show loading
    btn.style.display = 'none';
    loader.style.display = 'inline-block';

    const campaignData = {
        name: document.getElementById('campaign-name').value,
        description: document.getElementById('campaign-description').value,
        target_criteria: {
            industry: document.getElementById('industry').value,
            location: document.getElementById('location').value,
            company_size: document.getElementById('company-size').value
        }
    };

    try {
        const response = await fetch(`${API_BASE_URL}/campaigns`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(campaignData)
        });

        if (response.ok) {
            showToast('Campaign created successfully!', 'success');
            document.getElementById('campaign-form').reset();
            loadCampaigns();
            loadStats();
        } else {
            const error = await response.json();
            showToast(`Error: ${error.detail}`, 'error');
        }
    } catch (error) {
        showToast('Failed to create campaign', 'error');
        console.error(error);
    } finally {
        btn.style.display = 'inline';
        loader.style.display = 'none';
    }
}

// Load Campaigns
async function loadCampaigns() {
    const container = document.getElementById('campaigns-list');
    container.innerHTML = '<div class="text-center py-6 text-gray-500"><div class="text-3xl mb-2">⏳</div><p class="text-sm">Loading campaigns...</p></div>';

    try {
        const response = await fetch(`${API_BASE_URL}/campaigns`);
        const data = await response.json();

        if (data.items && data.items.length > 0) {
            // Show only first 6 campaigns
            const displayCampaigns = data.items.slice(0, 6);

            container.innerHTML = '<div class="grid grid-cols-1 md:grid-cols-2 gap-3">' +
                displayCampaigns.map(campaign => {
                    const statusColors = {
                        active: 'badge-success',
                        draft: 'badge-warning',
                        completed: 'badge-info',
                        paused: 'badge-danger'
                    };

                    return `
                <div class="campaign-card rounded-lg p-3 shadow-sm hover:shadow-md transition-all duration-300">
                    <div class="flex items-start justify-between mb-2">
                        <div class="flex-1 min-w-0">
                            <h3 class="text-sm font-bold text-gray-800 mb-0 truncate">${campaign.name}</h3>
                            <p class="text-gray-500 text-xs truncate">${campaign.description || 'No description'}</p>
                        </div>
                        <span class="badge ${statusColors[campaign.status] || 'badge-info'} text-xs ml-2 flex-shrink-0">
                            ${campaign.status.toUpperCase()}
                        </span>
                    </div>
                    
                    <div class="grid grid-cols-4 gap-2 mb-2">
                        <div class="text-center">
                            <div class="text-lg font-bold text-purple-600">${campaign.total_leads}</div>
                            <div class="text-xs text-gray-500">Leads</div>
                        </div>
                        <div class="text-center">
                            <div class="text-lg font-bold text-blue-600">${campaign.qualified_leads}</div>
                            <div class="text-xs text-gray-500">Qual.</div>
                        </div>
                        <div class="text-center">
                            <div class="text-lg font-bold text-green-600">${campaign.emails_sent}</div>
                            <div class="text-xs text-gray-500">Sent</div>
                        </div>
                        <div class="text-center">
                            <div class="text-lg font-bold text-pink-600">${campaign.emails_replied}</div>
                            <div class="text-xs text-gray-500">Replies</div>
                        </div>
                    </div>
                    
                    <div class="flex gap-1">
                        <button class="flex-1 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-semibold py-1 px-2 rounded text-xs transition" onclick="runCampaign(${campaign.id})">
                            ▶️ Run
                        </button>
                        <button class="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-1 px-2 rounded text-xs transition" onclick="viewCampaignLeads(${campaign.id})">
                            👥 Leads
                        </button>
                        <button class="bg-red-500 hover:bg-red-600 text-white font-semibold py-1 px-2 rounded text-xs transition" onclick="deleteCampaign(${campaign.id})">
                            🗑️
                        </button>
                    </div>
                </div>
                `;
                }).join('') + '</div>';

            // Add "Show More" button if there are more campaigns
            if (data.items.length > 6) {
                container.innerHTML += `
                    <div class="text-center mt-3">
                        <button onclick="showAllCampaigns()" class="text-purple-600 hover:text-purple-800 text-sm font-semibold">
                            Show ${data.items.length - 6} more campaigns ↓
                        </button>
                    </div>
                `;
            }
        } else {
            container.innerHTML = `
                <div class="text-center py-8">
                    <div class="text-5xl mb-3">📭</div>
                    <p class="text-gray-600 text-base font-medium">No campaigns yet</p>
                    <p class="text-gray-500 text-xs">Create your first campaign above!</p>
                </div>
            `;
        }
    } catch (error) {
        container.innerHTML = '<div class="text-center py-6 text-red-500"><div class="text-3xl mb-2">❌</div><p class="text-sm">Error loading campaigns</p></div>';
        console.error(error);
    }
}

// Run Campaign
async function runCampaign(campaignId) {
    if (!confirm('Run this campaign? This will generate leads and emails.')) return;

    showToast('Running campaign... This may take a few minutes.', 'info');

    try {
        const response = await fetch(`${API_BASE_URL}/campaigns/${campaignId}/run`, {
            method: 'POST'
        });

        if (response.ok) {
            const result = await response.json();
            showToast(`Campaign completed! ${result.data?.leads_found || 0} leads found.`, 'success');
            loadCampaigns();
            loadLeads();
            loadStats();
        } else {
            const error = await response.json();
            showToast(`Error: ${error.detail}`, 'error');
        }
    } catch (error) {
        showToast('Failed to run campaign', 'error');
        console.error(error);
    }
}

// Load Leads
async function loadLeads() {
    const container = document.getElementById('leads-list');
    container.innerHTML = '<div class="text-center py-8 text-gray-500"><div class="text-4xl mb-2">⏳</div><p>Loading leads...</p></div>';

    try {
        const response = await fetch(`${API_BASE_URL}/leads?limit=10`);
        const data = await response.json();

        if (data.items && data.items.length > 0) {
            container.innerHTML = '<div class="overflow-x-auto"><table class="min-w-full"><thead class="bg-gray-50"><tr><th class="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Company</th><th class="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Quality</th><th class="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Industry</th><th class="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Location</th><th class="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Contact</th></tr></thead><tbody class="bg-white divide-y divide-gray-200">' +
                data.items.map(lead => {
                    const qualityColors = {
                        hot: 'badge-danger',
                        warm: 'badge-warning',
                        cold: 'badge-info'
                    };

                    const qualityIcons = {
                        hot: '🔥',
                        warm: '⭐',
                        cold: '❄️'
                    };

                    return `
                    <tr class="hover:bg-gray-50 transition">
                        <td class="px-6 py-4">
                            <div class="text-sm font-semibold text-gray-900">${lead.company_name}</div>
                            ${lead.quality_score ? `<div class="text-xs text-gray-500">Score: ${(lead.quality_score * 100).toFixed(0)}%</div>` : ''}
                        </td>
                        <td class="px-6 py-4">
                            ${lead.quality ? `<span class="badge ${qualityColors[lead.quality]}">${qualityIcons[lead.quality]} ${lead.quality.toUpperCase()}</span>` : '<span class="text-gray-400 text-sm">-</span>'}
                        </td>
                        <td class="px-6 py-4 text-sm text-gray-700">
                            ${lead.industry || '<span class="text-gray-400">-</span>'}
                        </td>
                        <td class="px-6 py-4 text-sm text-gray-700">
                            ${lead.location || '<span class="text-gray-400">-</span>'}
                        </td>
                        <td class="px-6 py-4 text-sm text-gray-700">
                            ${lead.contact_email ? `<a href="mailto:${lead.contact_email}" class="text-purple-600 hover:text-purple-800">📧 ${lead.contact_email}</a>` : '<span class="text-gray-400">-</span>'}
                        </td>
                    </tr>
                    `;
                }).join('') + '</tbody></table></div>';
        } else {
            container.innerHTML = `
                <div class="text-center py-12">
                    <div class="text-6xl mb-4">👥</div>
                    <p class="text-gray-600 text-lg font-medium">No leads yet</p>
                    <p class="text-gray-500 text-sm">Run a campaign to generate leads!</p>
                </div>
            `;
        }
    } catch (error) {
        container.innerHTML = '<div class="text-center py-8 text-red-500"><div class="text-4xl mb-2">❌</div><p>Error loading leads</p></div>';
        console.error(error);
    }
}

// View Campaign Leads
async function viewCampaignLeads(campaignId) {
    try {
        const response = await fetch(`${API_BASE_URL}/leads?campaign_id=${campaignId}`);
        const data = await response.json();

        showToast(`Found ${data.total} leads for this campaign`, 'info');

        // Scroll to leads section
        document.getElementById('leads-list').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        showToast('Error loading campaign leads', 'error');
    }
}

// Delete Campaign
async function deleteCampaign(campaignId) {
    if (!confirm('Delete this campaign? This cannot be undone.')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/campaigns/${campaignId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showToast('Campaign deleted successfully', 'success');
            loadCampaigns();
            loadStats();
        } else {
            showToast('Error deleting campaign', 'error');
        }
    } catch (error) {
        showToast('Failed to delete campaign', 'error');
        console.error(error);
    }
}