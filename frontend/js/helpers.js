// Show All Campaigns Function
async function showAllCampaigns() {
    const container = document.getElementById('campaigns-list');
    container.innerHTML = '<div class="text-center py-6 text-gray-500"><div class="text-3xl mb-2">⏳</div><p class="text-sm">Loading all campaigns...</p></div>';

    try {
        const response = await fetch(`${API_BASE_URL}/campaigns`);
        const data = await response.json();

        if (data.items && data.items.length > 0) {
            container.innerHTML = '<div class="grid grid-cols-1 md:grid-cols-2 gap-3">' +
                data.items.map(campaign => {
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

            // Add "Show Less" button
            container.innerHTML += `
                <div class="text-center mt-3">
                    <button onclick="loadCampaigns()" class="text-purple-600 hover:text-purple-800 text-sm font-semibold">
                        Show less ↑
                    </button>
                </div>
            `;
        }
    } catch (error) {
        container.innerHTML = '<div class="text-center py-6 text-red-500"><div class="text-3xl mb-2">❌</div><p class="text-sm">Error loading campaigns</p></div>';
        console.error(error);
    }
}
