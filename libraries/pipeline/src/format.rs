//! 配置文件格式处理

use crate::config::Config;
use std::io::Read;
use std::str::FromStr;
use utils::normalize_path;

/// 支持的配置文件格式
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConfigFormat {
    Yaml,
    Json,
    Toml,
}

/// 从字符串读取配置
pub fn read_config(content: &str, format: ConfigFormat) -> Result<Config, Box<dyn std::error::Error>> {
    match format {
        ConfigFormat::Yaml => {
            let config: Config = serde_yaml::from_str(content)?;
            Ok(config)
        }
        ConfigFormat::Json => {
            let config: Config = serde_json::from_str(content)?;
            Ok(config)
        }
        ConfigFormat::Toml => {
            let config: Config = toml::from_str(content)?;
            Ok(config)
        }
    }
}

/// 从文件读取配置
pub fn read_config_from_file<P: AsRef<std::path::Path>>(
    path: P,
    format: ConfigFormat,
) -> Result<Config, Box<dyn std::error::Error>> {
    let path = normalize_path(path)?;
    let content = std::fs::read_to_string(&path)?;
    read_config(&content, format)
}

/// 将配置写入字符串
pub fn write_config(config: &Config, format: ConfigFormat) -> Result<String, Box<dyn std::error::Error>> {
    match format {
        ConfigFormat::Yaml => {
            let yaml = serde_yaml::to_string(config)?;
            Ok(yaml)
        }
        ConfigFormat::Json => {
            let json = serde_json::to_string_pretty(config)?;
            Ok(json)
        }
        ConfigFormat::Toml => {
            let toml = toml::to_string(config)?;
            Ok(toml)
        }
    }
}

/// 将配置写入文件
pub fn write_config_to_file<P: AsRef<std::path::Path>>(
    config: &Config,
    path: P,
    format: ConfigFormat,
) -> Result<(), Box<dyn std::error::Error>> {
    let path = normalize_path(path)?;
    let content = write_config(config, format)?;
    std::fs::write(path, content)?;
    Ok(())
}

/// 从 reader 读取配置
pub fn read_config_from_reader<R: Read>(
    reader: R,
    format: ConfigFormat,
) -> Result<Config, Box<dyn std::error::Error>> {
    match format {
        ConfigFormat::Yaml => {
            let config: Config = serde_yaml::from_reader(reader)?;
            Ok(config)
        }
        ConfigFormat::Json => {
            let config: Config = serde_json::from_reader(reader)?;
            Ok(config)
        }
        ConfigFormat::Toml => {
            let mut reader = reader;
            let mut content = String::new();
            reader.read_to_string(&mut content)?;
            let config: Config = toml::from_str(&content)?;
            Ok(config)
        }
    }
}

impl FromStr for ConfigFormat {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.to_lowercase().as_str() {
            "yaml" | "yml" => Ok(ConfigFormat::Yaml),
            "json" => Ok(ConfigFormat::Json),
            "toml" => Ok(ConfigFormat::Toml),
            _ => Err(format!("Unsupported format: {}", s)),
        }
    }
}

impl std::fmt::Display for ConfigFormat {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ConfigFormat::Yaml => write!(f, "yaml"),
            ConfigFormat::Json => write!(f, "json"),
            ConfigFormat::Toml => write!(f, "toml"),
        }
    }
}