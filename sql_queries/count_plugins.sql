SELECT COUNT(PluginId) AS PluginIdCount
FROM TenablePluginData
WHERE CVEID IS NOT NULL;